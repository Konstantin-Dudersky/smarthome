"""Типы данных."""

from asyncio import sleep as asleep
from enum import Enum
from typing import Any, Coroutine

from pydantic import BaseModel


class Qual(Enum):
    """Коды качества сигнала."""

    BAD = 0
    GOOD = 80


class Units(Enum):
    """Единицы измерения."""

    NOUNIT = 0
    KELVIN = 1000
    DEG_CELSIUS = 1001
    LUX = 1314
    PERCENT = 1342


class Scale:
    """Диапазон измерения сигнала."""

    class Schema(BaseModel):
        """Схема для API."""

        low: float
        high: float

    def __init__(self: "Scale", low: float = 0, high: float = 100.0) -> None:
        """Диапазон измерения сигнала.

        :param low: нижний предел
        :param high: верхний предел
        """
        self.__low = low
        self.__high = high

    @property
    def schema(self: "Scale") -> Schema:
        """Схема для API.

        :return: схема для API
        """
        return self.Schema(low=self.__low, high=self.__high)


# SigBase ---------------------------------------------------------------------


class SigBase:
    """Базовый класс для сигналов."""

    class Schema(BaseModel):
        """Схема для API."""

        qual: Qual

    def __init__(self: "SigBase", qual: Qual) -> None:
        """Базовый класс для сигналов.

        :param qual: качество
        """
        self._qual = qual
        self._coro_read: Coroutine[Any, Any, None] | None = None
        self._coro_write: Coroutine[Any, Any, None] | None = None

    async def read_exec(self: "SigBase") -> None:
        """Выполнить чтение данных.

        :return: None
        """
        if self._coro_read is None:
            return await asleep(0)
        await self._coro_read
        self._coro_read = None
        return await asleep(0)

    async def write_exec(self: "SigBase") -> None:
        """Выполнить запись данных.

        :return: None
        """
        if self._coro_write is None:
            return await asleep(0)
        await self._coro_write
        self._coro_write = None
        return await asleep(0)

    @property
    def qual(self: "SigBase") -> Qual:
        """Возвращает качество.

        :return: качество
        """
        return self._qual

    @qual.setter
    def qual(self: "SigBase", value: Qual) -> None:
        """Устанавливает качество.

        :param value: новое качество
        """
        self._qual = value


# SigBool ---------------------------------------------------------------------


class SigBool(SigBase):
    """Дискретный сигнал."""

    class Schema(SigBase.Schema):
        """Схема для API."""

        value: bool

    def __init__(
        self: "SigBool",
        value: bool = False,
        qual: Qual = Qual.BAD,
    ) -> None:
        """Дискретное значение.

        :param value: начальное значение
        :param qual: качество
        """
        super().__init__(qual)
        self.__value = value

    def __str__(self: "SigBool") -> str:
        """Строковое предстваление.

        :return: строковое представление
        """
        return f"({self.__value}, {self.qual.name})"

    @property
    def value(self: "SigBool") -> bool:
        """Возвращает значение.

        :return: значение
        """
        return self.__value

    @value.setter
    def value(self: "SigBool", value: bool) -> None:
        """Устанавливает значение.

        :param value: новое значение
        """
        self.__value = value

    @property
    def schema(
        self: "SigBool",
    ) -> Schema:
        """Схема для API.

        :return: схема для API
        """
        return self.Schema(
            value=self.value,
            qual=self.qual,
        )

    def update(
        self: "SigBool",
        value: bool | None = None,
        qual: Qual | None = None,
    ) -> None:
        """Обновить значение или качество.

        :param value: значение
        :param qual: качество
        """
        if value is not None:
            self.__value = value
        if qual is not None:
            self.qual = qual


# SigFloat --------------------------------------------------------------------


class SigFloat(SigBase):
    """Дискретный сигнал."""

    class Schema(SigBase.Schema):
        """Схема для API."""

        value: float
        unit: Units
        scale: Scale.Schema

    def __init__(
        self: "SigFloat",
        value: float = 0.0,
        unit: Units = Units.DEG_CELSIUS,
        qual: Qual = Qual.BAD,
        scale: Scale = Scale(0, 100.0),
    ) -> None:
        """Вещественное значение.

        :param value: значение
        :param unit: единица измерения
        :param qual: качество
        :param scale: диапазон сигнала
        """
        super().__init__(qual)
        self.__value = value
        self.__unit = unit
        self.__scale = scale

    def __str__(self: "SigFloat") -> str:
        """Строковое предстваление.

        :return: строковое представление
        """
        return f"({self.__value}{self.__unit.value}, {self.qual.name})"

    @property
    def value(self: "SigFloat") -> float:
        """Возвращает значение.

        :return: значение
        """
        return self.__value

    @value.setter
    def value(self: "SigFloat", value: float) -> None:
        """Устанавливает значение.

        :param value: новое значение
        """
        self.__value = value

    @property
    def unit(self: "SigFloat") -> Units:
        """Возвращает единицу измерения.

        :return: единица измерения
        """
        return self.__unit

    @property
    def schema(
        self: "SigFloat",
    ) -> Schema:
        """Схема для API.

        :return: схема для API
        """
        return self.Schema(
            value=self.value,
            unit=self.unit,
            qual=self.qual,
            scale=self.__scale.schema,
        )

    def update(
        self: "SigFloat",
        value: float | None = None,
        qual: Qual | None = None,
    ) -> None:
        """Обновить значение или качество.

        :param value: значение
        :param qual: качество
        """
        if value is not None:
            self.__value = value
        if qual is not None:
            self.qual = qual
