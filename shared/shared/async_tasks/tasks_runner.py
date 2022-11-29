"""Класс для запуска асинхронных задач."""

import asyncio
import logging
from typing import Final, Iterable

from .tasks_protocol import TasksProtocol

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

MSG_BASE_EXCEPTION: Final[
    str
] = "Необработанное исключение, программа заканчивает выполнение"


class TasksRunner(object):
    """Класс для запуска асинхронных задач."""

    def __init__(
        self,
        objects_with_tasks: Iterable[TasksProtocol],
        return_when: str = asyncio.FIRST_COMPLETED,
    ) -> None:
        """Класс для запуска асинхронных задач.

        Parameters
        ----------
        objects_with_tasks: Iterable[TasksProtocol]
            Перечень объектов с реализованным интерфейсом TasksProtocol
        return_when: str
            Условие остановки выполнения
        """
        self.__objects_with_tasks = objects_with_tasks
        self.__return_when = return_when

    async def __call__(self) -> None:
        """Запуск задач."""
        tasks = self.__create_tasks_for_coro(
            self.__objects_with_tasks,
        )
        done_tasks, _ = await asyncio.wait(
            tasks,
            return_when=self.__return_when,
        )
        try:
            [task.result() for task in done_tasks]  # noqa: WPS428
        except BaseException:  # noqa: WPS424
            log.exception(MSG_BASE_EXCEPTION)

    def __create_tasks_for_coro(
        self,
        objects_with_tasks: Iterable[TasksProtocol],
    ) -> set[asyncio.Task[None]]:
        tasks: set[asyncio.Task[None]] = set()
        for obj_with_tasks in objects_with_tasks:
            for task in obj_with_tasks.async_tasks:
                tasks.add(asyncio.create_task(task))
        return tasks
