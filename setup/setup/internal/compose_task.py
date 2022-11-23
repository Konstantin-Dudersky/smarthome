"""Составная задача."""

import logging
from typing import Final, List

from .base_task import BaseTask

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

CHAR_WIDTH: Final[int] = 80


class ComposeTask(object):
    """Составная задача."""

    def __init__(
        self,
        desc: str,
        subtasks: List[BaseTask],
    ) -> None:
        """Составная задача.

        Parameters
        ----------
        desc: str
            Описание задачи
        subtasks: List[BaseTask]
            список задач
        """
        self.__desc = desc
        self.__subtasks = subtasks
        self.__command: str = ""

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
        log.info(
            "{name} - {desc}:\n".format(
                name=self.name,
                desc=self.desc,
            ),
        )
        for task in self.__subtasks:
            task.execute()

    def __repr__(self) -> str:
        """Строковое представление.

        Returns
        -------
        строковое представление.
        """
        out: str = "* {name} - {desc}:\n".format(
            name=self.name,
            desc=self.desc,
        )
        for task in self.__subtasks:
            out += "\t* {0}\n".format(task)
        return out
