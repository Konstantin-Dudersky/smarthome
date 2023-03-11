"""Сообщения для передачи через брокер сообщений."""

from typing import Type

from .base_message import BaseMessage
from .open_close_sensor import OpenCloseSensor
from .temperature_sensor import TemperatureSensor

__all__ = [
    "BaseMessage",
    "OpenCloseSensor",
    "TemperatureSensor",
]


# TODO - сделать через декоратор
dict_messages: dict[str, Type[BaseMessage]] = {
    "OpenCloseSensor": OpenCloseSensor,
    "TemperatureSensor": TemperatureSensor,
}
