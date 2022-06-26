"""Типы данных."""

from enum import Enum, auto


class Qual(Enum):
    """Коды качества сигнала."""

    BAD = auto()
    GOOD = auto()


class Di:
    """Дискретное значение."""

    def __init__(
        self: "Di",
        value: bool = False,
        qual: Qual = Qual.GOOD,
    ) -> None:
        """Дискретное значение.

        :param value: значение
        :param qual: качество
        """
        self.__value = value
        self.__qual = qual

    def __str__(self: "Di") -> str:
        """Строковое предстваление.

        :return: строковое представление
        """
        return f"({self.__value}, {self.__qual.name})"

    @property
    def value(self: "Di") -> bool:
        """Возвращает значение.

        :return: значение
        """
        return self.__value

    @value.setter
    def value(self: "Di", value: bool) -> None:
        """Устанавливает значение.

        :param value: новое значение
        """
        self.__value = value

    @property
    def qual(self: "Di") -> Qual:
        """Возвращает качество.

        :return: качество
        """
        return self.__qual

    @qual.setter
    def qual(self: "Di", value: Qual) -> None:
        """Устанавливает качество.

        :param value: новое качество
        """
        self.__qual = value

    def update(
        self: "Di",
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
            self.__qual = qual
