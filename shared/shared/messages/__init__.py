"""Сообщения для передачи через брокер сообщений."""

from .base_message import BaseMessage
from .binary_sensor import BinarySensor

__all__ = [
    "BaseMessage",
    "BinarySensor",
]