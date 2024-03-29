"""Хранение данных с датчика."""

import abc
import datetime as dt
import logging
from typing import Generic, Type, TypeVar

from pydantic import BaseModel, Field, ValidationError

from shared.simple_deque import ISimpleDequeAppend

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class BaseSensorConfigModel(BaseModel):
    """Базовая модель конфигурации."""


class BaseSensorStateModel(BaseModel):
    """Базовая модель состояния."""

    lastupdated: dt.datetime | None = dt.datetime.min


class BaseSensorModel(BaseModel):
    """Базовая модель состояния."""

    config: BaseSensorConfigModel = BaseSensorConfigModel.construct()
    state: BaseSensorStateModel = BaseSensorStateModel.construct()
    etag: str = ""
    manufacturername: str = ""
    modelid: str = ""
    name: str = ""
    swversion: str = ""
    type_: str = Field(default="", alias="type")
    uniqueid: str = ""


TSensor = TypeVar("TSensor", bound=BaseSensorModel)


class BaseSensor(abc.ABC, Generic[TSensor]):
    """Датчик."""

    def __init__(
        self,
        uniqueid: str,
        name: str,
        model: Type[TSensor],
        model_state: Type[BaseSensorStateModel],
    ) -> None:
        """Сенсор."""
        self.__uniqueid = uniqueid
        self.__name = name
        self.__model = model
        self.__model_state = model_state

        self._data = model.construct()
        self._messagebus: ISimpleDequeAppend[str] | None = None

    def __repr__(self) -> str:
        """Represent as string."""
        return str(self._data.dict(by_alias=True))

    @property
    def uniqueid(self) -> str:
        """Идентификатор."""
        return self.__uniqueid

    @property
    def name(self) -> str:
        """Название датчика."""
        return self.__name

    @property
    def sensor_data(self) -> TSensor:
        """Данные датчика."""
        return self._data

    @property
    def messagebus(self) -> ISimpleDequeAppend[str]:
        """Ссылка на шину сообщений."""
        if self._messagebus is None:
            msg: str = "Ссылка на шину сообщений на задана"
            log.error(msg)
            raise ValueError(msg)
        return self._messagebus

    @messagebus.setter
    def messagebus(self, messagebus: ISimpleDequeAppend[str]) -> None:
        self._messagebus = messagebus

    @abc.abstractmethod
    def create_messages(self) -> None:
        """Создать сообщения для передачи в брокер."""

    def update_data(self, message: str) -> None:
        """Обновить данные полностью.

        При опросе шлюза по API возвращаются все данные.
        """
        try:
            self._data = self.__model.parse_obj(message)
        except ValidationError as exc:
            log.error(
                "Error parsing:\nmessage: {0}\nerror:{1}".format(message, exc),
            )
            return
        self.create_messages()

    def update_state(self, message: str) -> None:
        """Обновить данные состояния.

        При опросе шлюза по websocket возвращается только состояние.
        """
        try:
            state = self.__model_state.parse_obj(message)
        except ValidationError as exc:
            log.error("Error parsing message:\n{0}".format(message))
            log.error(exc)
            return
        self._data.state = state
        self.create_messages()
