"""Хранение данных с датчика."""

import abc
import datetime as dt
from typing import Generic, Type, TypeVar

from pydantic import BaseModel, Field


class BaseSensorConfigModel(BaseModel):
    """Базовая модель конфигурации."""


class BaseSensorStateModel(BaseModel):
    """Базовая модель состояния."""

    lastupdated: dt.datetime = dt.datetime.min


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
        self.__data = model.construct()
        self.__model = model
        self.__model_state = model_state

    def __repr__(self) -> str:
        """Represent as string."""
        return str(self.__data.dict(by_alias=True))

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
        return self.__data

    def update_data(self, message: str) -> None:
        """Обновить данные полностью.

        При опросе шлюза по API возвращаются все данные.
        """
        self.__data = self.__model.parse_obj(message)

    def update_state(self, message: str) -> None:
        """Обновить данные состояния.

        При опросе шлюза по websocket возвращается только состояние.
        """
        state = self.__model_state.parse_obj(message)
        self.__data.state = state
