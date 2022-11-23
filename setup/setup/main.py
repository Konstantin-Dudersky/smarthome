import logging
import sys
from typing import Callable, List, NamedTuple, Optional

from ._shared import get_logger
from .internal.base_task import BaseTask
from .internal.compose_task import ComposeTask


log = get_logger(__name__, logging.DEBUG)


class Task:
    """Задача."""

    __desc: str
    __task: Callable[[], None]
    __command: str = ""
    __confirm: bool

    def __init__(
        self: "Task",
        desc: str,
        task: Callable[[], None],
        confirm: bool = True,
    ) -> None:
        """Задача."""
        self.__desc = desc
        self.__task = task
        self.__confirm = confirm

    @property
    def command(self: "Task") -> str:
        return self.__command

    @command.setter
    def command(self: "Task", value: str) -> None:
        self.__command = value

    def __str__(self: "Task") -> str:
        return f"* {self.__command} - {self.__desc}"

    def execute(self: "Task") -> None:
        """Выполнить задачу."""
        log.info("-" * 80)
        log.info(f"{self.__command} - {self.__desc}")
        if self.__confirm:
            while True:
                log.info("-> Выполнить ? (y/n)")
                ans = input()
                if ans == "y":
                    break
                elif ans == "n":
                    return
        self.__task()


def execute(
    arg: List[str],
    simple_tasks: NamedTuple,
    simple_env_tasks: Optional[NamedTuple],
    compose_tasks: NamedTuple,
) -> None:
    task: BaseTask
    compose_task: ComposeTask
    for name, task in simple_tasks._asdict().items():
        task.name = name
    # if simple_env_tasks is not None:
    #     for command, task in simple_env_tasks._asdict().items():
    #         task.command = command
    for name, compose_task in compose_tasks._asdict().items():
        compose_task.name = name
    if len(arg) <= 1:
        log.debug("\nЗадачи:")
        for st in simple_tasks:
            log.debug("* {0}".format(st))
        if simple_env_tasks is not None:
            log.debug("\nЗадачи вирт. окружения:")
            for ste in simple_env_tasks:
                log.debug("* - {0}".format(ste))
        log.debug("\nКомбинированные задачи:")
        for ct in compose_tasks:
            log.debug(ct)
        sys.exit(0)
    task_arg = arg[1]
    if task_arg in simple_tasks._asdict().keys():
        simple_task: BaseTask = simple_tasks._asdict()[task_arg]
        simple_task.execute()
        sys.exit(0)
    if simple_env_tasks is not None:
        if task_arg in simple_env_tasks._asdict().keys():
            simple_env_tasks._asdict()[task_arg].execute()
            sys.exit(0)
    if task_arg in compose_tasks._asdict().keys():
        compose_tasks._asdict()[task_arg].execute()
        sys.exit(0)
    log.error(f"Задача {task_arg} не найдена!")
