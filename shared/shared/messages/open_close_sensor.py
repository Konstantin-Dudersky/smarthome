"""Датчик открытия с двумя состояниями."""

from .base_message import BaseMessage


class OpenCloseSensor(BaseMessage):
    """Датчик с двумя состояниями."""

    opened: bool
