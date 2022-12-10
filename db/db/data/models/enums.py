"""Перечисления."""

from enum import StrEnum, auto


class AggEnum(StrEnum):
    """Типы аггрегации."""

    curr = auto()
    first = auto()
    inc = auto()
    sum = auto()
    mean = auto()
    min = auto()
    max = auto()


class StatusEnum(StrEnum):
    """Коды статуса."""

    good = auto()
    uncertain = auto()
    bad = auto()
