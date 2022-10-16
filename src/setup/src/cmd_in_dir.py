"""Выполнить команду в указанной папке."""

import logging
import os
import subprocess
from typing import Callable

log: logging.Logger = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def main(work_dir: str, command: str) -> Callable[[], None]:
    """Выполнить команду в папке.

    :param work_dir: относительный путь к папке
    :param command: команда
    :return: функция
    """

    def _main() -> None:
        curr_dir = os.getcwd()
        work_dir_abs_full = os.path.join(curr_dir, work_dir)
        work_dir_abs = os.path.abspath(work_dir_abs_full)
        log.info(f"Рабочая папка: {work_dir_abs}")
        os.chdir(work_dir_abs)
        log.info(f"Выполняем команду: {command}")
        subprocess.run(command.split(" "))
        os.chdir(curr_dir)

    return _main
