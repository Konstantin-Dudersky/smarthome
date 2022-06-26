"""Логические функции."""

from copy import copy
import time

from .types import SigBool, Qual


class CyclicRun:
    """Циклическое выполнение."""

    def __init__(self: "CyclicRun", time_between: float = 1.0) -> None:
        """Циклическое выполнение.

        :param time_between: Время между вызовами, [s]
        """
        self.__last_call = 0
        self.__time_between = int(time_between * 1e9)
        self.__started = False

    @property
    def started(self: "CyclicRun") -> bool:
        """Запускалась ли функция run хотя бы раз.

        :return: True - функция run выполнялась
        """
        return self.__started

    def __call__(self: "CyclicRun") -> bool:
        """Проверка, что время истекло.

        Нужно циклически вызывать.

        :return: True - время истекло
        """
        self.__started = True
        now = time.perf_counter_ns()
        if (now - self.__last_call) > self.__time_between:
            self.__last_call = now
            return True
        return False


class PosFront:
    """Положительный фронт."""

    def __init__(self: "PosFront") -> None:
        """Положительный фронт."""
        self.__prev = SigBool(False, Qual.BAD)

    def __call__(self: "PosFront", pv_in: SigBool) -> SigBool:
        """Проверка изменения сигнала.

        :param pv_in: проверяемый сигнал
        :return: True если проверяемый сигнал перешел из False в True
        """
        res = SigBool()
        if pv_in.qual != Qual.GOOD or self.__prev.qual != Qual.GOOD:
            res = SigBool(False, Qual.BAD)
        if pv_in.value and not self.__prev.value:
            res = SigBool(True, Qual.GOOD)
        self.__prev = copy(pv_in)
        return res


class NegFront:
    """Отрицательный фронт."""

    def __init__(self: "NegFront") -> None:
        """Отрицательный фронт."""
        self.__prev = SigBool(False, Qual.BAD)

    def __call__(self: "NegFront", pv_in: SigBool) -> SigBool:
        """Проверка изменения сигнала.

        :param pv_in: проверяемый сигнал
        :return: True если проверяемый сигнал перешел из True в False
        """
        res = SigBool()
        if pv_in.qual != Qual.GOOD or self.__prev.qual != Qual.GOOD:
            res = SigBool(False, Qual.BAD)
        if not pv_in.value and self.__prev.value:
            res = SigBool(True, Qual.GOOD)
        self.__prev = copy(pv_in)
        return res
