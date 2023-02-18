"""Выполнение команды на целевой системе через SSH."""

import logging
import os
from typing import Final

from ..internal.base_task import BaseTask

_log = logging.getLogger(__name__)
_log.setLevel(logging.DEBUG)


CMD: Final[str] = "ssh -t {user}@{host} 'cd {folder} && {command}'"


class RemoteCommand(BaseTask):
    """Выполнение команды на целевой системе через SSH."""

    def __init__(
        self,
        desc: str,
        command: str,
        need_confirm: bool = True,
        remote_user: str = "root",
        remote_host: str = "target",
        remote_folder: str = "/home/code",
    ) -> None:
        """Выполнение команды на целевой системе через SSH."""
        super().__init__(desc, need_confirm)
        self.__command = command
        self.__remote_user = remote_user
        self.__remote_host = remote_host
        self.__remote_folder = remote_folder

    def _execute(self) -> None:
        cmd = CMD.format(
            user=self.__remote_user,
            host=self.__remote_host,
            folder=self.__remote_folder,
            command=self.__command,
        )
        _log.info("Выполняем команду:\n{0}".format(cmd))
        os.system(cmd)
