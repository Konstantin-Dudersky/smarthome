"""Логические функции."""

from copy import copy

from .types import Di, Qual


class PosFront:
    """Положительный фронт."""

    def __init__(self: "PosFront") -> None:
        """Положительный фронт."""
        self.__prev = Di(False, Qual.BAD)

    def __call__(self: "PosFront", pv_in: Di) -> Di:
        """Проверка изменения сигнала.

        :param pv_in: проверяемый сигнал
        :return: True если проверяемый сигнал перешел из False в True
        """
        res = Di()
        if pv_in.qual != Qual.GOOD or self.__prev.qual != Qual.GOOD:
            res = Di(False, Qual.BAD)
        if pv_in.value and not self.__prev.value:
            res = Di(True, Qual.GOOD)
        self.__prev = copy(pv_in)
        return res


class NegFront:
    """Отрицательный фронт."""

    def __init__(self: "NegFront") -> None:
        """Отрицательный фронт."""
        self.__prev = Di(False, Qual.BAD)

    def __call__(self: "NegFront", pv_in: Di) -> Di:
        """Проверка изменения сигнала.

        :param pv_in: проверяемый сигнал
        :return: True если проверяемый сигнал перешел из True в False
        """
        res = Di()
        if pv_in.qual != Qual.GOOD or self.__prev.qual != Qual.GOOD:
            res = Di(False, Qual.BAD)
        if not pv_in.value and self.__prev.value:
            res = Di(True, Qual.GOOD)
        self.__prev = copy(pv_in)
        return res
