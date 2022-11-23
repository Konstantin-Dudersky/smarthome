"""Выполнить команду."""

import logging
import os
import subprocess
from pathlib import Path

from .internal.base_task import BaseTask

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class SimpleCommand(BaseTask):
    """Выполнить команду в указанной папке."""

    def __init__(
        self,
        desc: str,
        command: str,
        work_dir_rel: str = ".",
        need_confirm: bool = True,
    ) -> None:
        """Выполнить команду в указанной папке.

        Parameters
        ----------
        desc: str
            Описание задачи
        need_confirm: bool
            Требуется подтверждение запуска
        work_dir_rel: str
            Относительный путь к папке
        command: str
            команда для запуска
        """
        super().__init__(desc, need_confirm)
        self.__command = command
        self.__work_dir_rel = work_dir_rel

    def _execute(self) -> None:
        curr_dir = os.getcwd()
        work_dir_abs = Path(self.__work_dir_rel).resolve()
        log.info("Рабочая папка: {0}".format(work_dir_abs))
        os.chdir(work_dir_abs)
        log.info("Выполняем команду: {0}".format(self.__command))
        subprocess.run(self.__command.split())
        os.chdir(curr_dir)
