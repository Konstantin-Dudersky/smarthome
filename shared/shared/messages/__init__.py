"""Сообщения для передачи через брокер сообщений."""

from typing import Type

from .base_message import (
    BaseMessage,
    HumiditySensor,
    LightLevel,
    OpenCloseSensor,
    PresenceSensor,
    PressureSensor,
    TemperatureSensor,
)

__all__ = [
    "BaseMessage",
    "HumiditySensor",
    "LightLevel",
    "OpenCloseSensor",
    "PresenceSensor",
    "PressureSensor",
    "TemperatureSensor",
]


# TODO - сделать через декоратор
dict_messages: dict[str, Type[BaseMessage]] = {
    "HumiditySensor": HumiditySensor,
    "LightLevel": LightLevel,
    "OpenCloseSensor": OpenCloseSensor,
    "PresenceSensor": PresenceSensor,
    "PressureSensor": PressureSensor,
    "TemperatureSensor": TemperatureSensor,
}
