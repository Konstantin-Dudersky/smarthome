"""Общие пакеты для проекта."""

from .logger import Logger
from . import messages

__all__: list[str] = [
    "Logger",
    "messages",
]
