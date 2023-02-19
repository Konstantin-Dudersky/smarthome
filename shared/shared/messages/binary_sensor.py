"""Датчик с двумя состояниями."""

from .base_message import BaseMessage


class BinarySensor(BaseMessage):
    """Датчик с двумя состояниями."""

    message_type: str = "BinarySensor"
    opened: bool
