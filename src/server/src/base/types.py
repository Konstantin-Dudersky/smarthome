"""Типы данных."""

from enum import Enum, auto


class Qual(Enum):
    """Коды качества сигнала."""

    BAD = auto()
    GOOD = auto()


class SigBase:
    """Базовый класс для сигналов."""

    def __init__(self: "SigBase", qual: Qual = Qual.GOOD) -> None:
        """Базовый класс для сигналов.

        :param qual: качество
        """
        self._qual = qual

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


class SigBool(SigBase):
    """Дискретный сигнал."""

    def __init__(
        self: "SigBool",
        value: bool = False,
        qual: Qual = Qual.GOOD,
    ) -> None:
        """Дискретное значение.

        :param value: значение
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
