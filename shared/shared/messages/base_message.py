"""Базовый класс сообщения."""

import datetime as dt

from typing import Self, Type

from pydantic import BaseModel, validator


class BaseMessage(BaseModel):
    """Базовый класс сообщения."""

    entity_id: str
    class_name: str | None = None
    ts: dt.datetime

    @validator("class_name", pre=True, always=True)
    def validate_class_name(
        cls: Type[Self],  # type: ignore
        class_name: str | None,
    ) -> str:
        """Установить имя класса."""
        return class_name or cls.__name__


class OpenCloseSensor(BaseMessage):
    """Датчик с двумя состояниями."""

    opened: bool


class TemperatureSensor(BaseMessage):
    """Датчик температуры."""

    temperature: float


class HumiditySensor(BaseMessage):
    """Датчик температуры."""

    humidity: float


class PressureSensor(BaseMessage):
    """Датчик температуры."""

    pressure: float


class PresenceSensor(BaseMessage):
    """Датчик присутствия."""

    presence: bool


class LightLevel(BaseMessage):
    """Датчик освещенности."""

    lux: float
