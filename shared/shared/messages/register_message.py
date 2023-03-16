"""Декоратор для регистрации классов сообщений в словарь.

Ключи словаря - названия классов.
Значения словаря - тип класса.
"""

from typing import Final, TypeVar

from .base_message import BaseMessage

messages_dict: dict[str, type[BaseMessage]] = {}

MSG: Final[
    str
] = "Классы сообщений должны иметь разные имена, дублирование: {0}"

MessageT = TypeVar("MessageT")


def register_message(cls: type[MessageT]) -> type[MessageT]:
    """Декоратор для регистрации классов сообщений в словарь."""
    name = cls.__name__
    if name in messages_dict:
        raise TypeError(MSG.format(name))
    messages_dict[name] = cls
    return cls
