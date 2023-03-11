"""Датчик температуры."""

from .base_message import BaseMessage


class TemperatureSensor(BaseMessage):
    """Датчик температуры."""

    temperature: float
