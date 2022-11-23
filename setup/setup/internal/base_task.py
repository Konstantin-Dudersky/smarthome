"""Абстрактный класс для задачи."""

import logging
from abc import ABC, abstractmethod
from typing import Final

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

CHAR_WIDTH: Final[int] = 80


def user_confirm() -> bool:
    """Подтверждение выполнения задачи пользователем.

    Returns
    -------
    True - выполняем задачу, False - прекращаем выполенение
    """
    while True:
        log.info("-> Выполнить ? (y/n)")
        ans = input()  # noqa: WPS421
        if ans == "y":
            return True
        elif ans == "n":
            return False


class BaseTask(ABC):
    """Базовый класс для задачи."""

    def __init__(self, desc: str, need_confirm: bool = True) -> None:
        """Базовый класс для задачи.

        Parameters
        ----------
        desc: str
            Описание задачи
        need_confirm: bool
            Требуется подтверждение запуска
        """
        self.__name: str | None = None
        self.__desc = desc
        self.__need_confirm = need_confirm

    def __repr__(self) -> str:
        """Строковое представление.

        Returns
        -------
        Строковое предствление
        """
        try:
            return "{name} - {desc}".format(
                name=self.name,
                desc=self.desc,
            )
        except ValueError:
            return self.desc

    @property
    def desc(self) -> str:
        """Описание задачи.

        Returns
        -------
        Описание задачи
        """
        return self.__desc

    @property
    def name(self) -> str:
        """Название задачи для запуска из консоли.

        Returns
        -------
        Название задачи

        Raises
        ------
        ValueError
            Название задачи не задано
        """
        if self.__name is None:
            raise ValueError("Название задачи не задано")
        return self.__name

    @name.setter
    def name(self, name: str) -> None:
        """Задать название задачи.

        Parameters
        ----------
        name: str
            Название задачи
        """
        self.__name = name

    def execute(self) -> None:
        """Функция для выполнения."""
        log.info("-" * CHAR_WIDTH)
        log.info(self)
        if self.__need_confirm:
            if not user_confirm():
                return
        self._execute()

    @abstractmethod
    def _execute(self) -> None:
        """Функция для выполнения, которую необходимо написать."""
