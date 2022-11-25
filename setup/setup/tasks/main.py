"""Запуск задач."""

import logging
from typing import List, NamedTuple

from ..internal.base_task import BaseTask
from ..internal.compose_task import ComposeTask
from ..internal.shared import get_logger

log = get_logger(__name__, logging.DEBUG)


class Runner(object):
    """Основной класс для запуска."""

    def __init__(
        self,
        args: List[str],
        simple_tasks: NamedTuple,
        compose_tasks: NamedTuple,
    ) -> None:
        """Основной класс для запуска."""
        self.__simple_tasks: dict[
            str,
            BaseTask,
        ] = simple_tasks._asdict()  # noqa: WPS437
        self.__compose_tasks: dict[
            str,
            ComposeTask,
        ] = compose_tasks._asdict()  # noqa: WPS437
        self.__save_task_names()
        if len(args) <= 1:
            self.__print()
            return
        task_name = args[1]
        if self.__try_start_simple_task(task_name):
            return
        if self.__try_start_compose_task(task_name):
            return
        log.error("Задача {0} не найдена!".format(task_name))

    def __save_task_names(self):
        for st_name, task in self.__simple_tasks.items():
            task.name = st_name
        for ct_name, compose_task in self.__compose_tasks.items():
            compose_task.name = ct_name

    def __print(self) -> None:
        log.debug("\nЗадачи:")
        for st in self.__simple_tasks.values():
            log.debug("* {0}".format(st))
        log.debug("\nКомбинированные задачи:")
        for ct in self.__compose_tasks.values():
            log.debug(ct)

    def __try_start_simple_task(self, task_name: str) -> bool:
        if task_name not in self.__simple_tasks.keys():
            return False
        simple_task: BaseTask = self.__simple_tasks[task_name]
        simple_task.execute()
        return True

    def __try_start_compose_task(self, task_name: str) -> bool:
        if task_name not in self.__compose_tasks.keys():
            return False
        compose_tasks: ComposeTask = self.__compose_tasks[task_name]
        compose_tasks.execute()
        return True
