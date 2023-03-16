"""Сообщения для передачи через брокер сообщений."""

from . import messages
from .base_message import BaseMessage
from .register_message import messages_dict

__all__ = [
    "BaseMessage",
    "messages",
    "messages_dict",
]
