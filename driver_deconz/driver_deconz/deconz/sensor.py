"""Хранение данных с датчика."""

from typing import Any, Generic, Type, TypeVar

from pydantic import BaseModel

TSensor = TypeVar("TSensor", bound=BaseModel)


class Sensor(Generic[TSensor]):
    """Датчик."""

    def __init__(
        self,
        identificator: int,
        name: str,
        model: Type[TSensor],
    ) -> None:
        """Сенсор."""
        self.__id = identificator
        self.__name = name
        self.__data = model.construct()
        self.__model = model

    @property
    def identificator(self) -> int:
        """Идентификатор."""
        return self.__id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def data(self) -> TSensor:
        """Данные датчика."""
        return self.__data

    def parse_data(self, message: dict[str, Any]):
        self.__data = self.__model.parse_obj(message)
