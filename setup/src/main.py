import logging
import sys
from typing import Callable, List, NamedTuple, Optional

from ._shared import get_logger

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


class ComposeTask:
    def __init__(
        self: "ComposeTask",
        desc: str,
        subtasks: List[Task],
    ) -> None:
        self.__desc = desc
        self.__subtasks = subtasks
        self.__command: str = ""

    @property
    def command(self: "ComposeTask") -> str:
        return self.__command

    @command.setter
    def command(self: "ComposeTask", value: str) -> None:
        self.__command = value

    def execute(self: "ComposeTask") -> None:
        log.info("-" * 80)
        log.info(f"{self.__command} - {self.__desc}")
        for task in self.__subtasks:
            task.execute()

    def __str__(self: "ComposeTask") -> str:
        out = f"* {self.__command} - {self.__desc}:\n"
        for task in self.__subtasks:
            out += f"\t{task}\n"
        return out


def execute(
    arg: List[str],
    simple_tasks: NamedTuple,
    simple_env_tasks: Optional[NamedTuple],
    compose_tasks: NamedTuple,
) -> None:
    for command, task in simple_tasks._asdict().items():
        task.command = command
    if simple_env_tasks is not None:
        for command, task in simple_env_tasks._asdict().items():
            task.command = command
    for command, task in compose_tasks._asdict().items():
        task.command = command
    if len(arg) <= 1:
        log.debug("\nЗадачи:")
        for task in simple_tasks:
            log.debug(task)
        if simple_env_tasks is not None:
            log.debug("\nЗадачи вирт. окружения:")
            for task in simple_env_tasks:
                log.debug(task)
        log.debug("\nКомбинированные задачи:")
        for task2 in compose_tasks:
            log.debug(task2)
        sys.exit(0)
    task_arg = arg[1]
    if task_arg in simple_tasks._asdict().keys():
        simple_tasks._asdict()[task_arg].execute()
        sys.exit(0)
    if simple_env_tasks is not None:
        if task_arg in simple_env_tasks._asdict().keys():
            simple_env_tasks._asdict()[task_arg].execute()
            sys.exit(0)
    if task_arg in compose_tasks._asdict().keys():
        compose_tasks._asdict()[task_arg].execute()
        sys.exit(0)
    log.error(f"Задача {task_arg} не найдена!")
