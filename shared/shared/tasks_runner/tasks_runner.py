"""Класс для запуска асинхронных задач."""

import asyncio
import logging
from typing import Final

from .protocols import TCoro, ITaskRunnerAdd

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

MSG_BASE_EXCEPTION: Final[
    str
] = "Необработанное исключение, программа заканчивает выполнение"


class TasksRunner(ITaskRunnerAdd):
    """Класс для запуска асинхронных задач."""

    def __init__(
        self,
        return_when: str = asyncio.FIRST_COMPLETED,
    ) -> None:
        """Класс для запуска асинхронных задач.

        Parameters
        ----------
        return_when: str
            Условие остановки выполнения
        """
        self.__coros: set[TCoro] = set()
        self.__return_when = return_when

    async def __call__(self) -> None:
        """Запуск задач."""
        tasks = self.__create_tasks_for_coro()
        done_tasks, _ = await asyncio.wait(
            tasks,
            return_when=self.__return_when,
        )
        try:
            [task.result() for task in done_tasks]  # noqa: WPS428
        except BaseException:  # noqa: WPS424
            log.exception(MSG_BASE_EXCEPTION)

    def add_task(self, name: str, coro: TCoro) -> None:
        """Добавить задачу для циклического.

        TODO: обернуть в бесконеченое циклическое выполнение
        """
        self.__coros.add(coro)

    def __create_tasks_for_coro(self) -> set[asyncio.Task[None]]:
        tasks: set[asyncio.Task[None]] = set()
        for coro in self.__coros:
            tasks.add(asyncio.create_task(coro))
        return tasks
