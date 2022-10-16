"""Работа с файлом настроек .env."""

import logging
import os
from typing import Callable

from .cmd_in_dir import main
from .docker_tasks import run_exec_remove
from ._shared import dir_rel_to_abs


log: logging.Logger = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def create(
    work_dir_rel: str = "../server",
    image: str = "image",
    mount: str | None = None,
    command: str = "poetry run poe create_env",
) -> Callable[[], None]:
    """Создать файл с настройками.

    :param work_dir_rel: относительный путь к папке
    :param command: команда
    :return: задача
    """

    def _task() -> None:
        log.info("Создаем файл с настройками")
        work_dir_abs = dir_rel_to_abs(work_dir_rel)
        log.info("Рабочая папка: %s", work_dir_abs)
        os.chdir(work_dir_abs)
        run_exec_remove(
            image=image,
            mount=mount,
            command=command,
        )()
        while True:
            log.warning(
                "Задайте настройки перед продолжением, после введите (y)",
            )
            ans: str = input()
            if ans == "y":
                break

    return _task


def export(
    work_path_rel: str = "../server",
    command: str = "poetry run poe export_env",
    export_path_rel: str = "../../docs",
    export_filename: str = "server_env.json",
) -> Callable[[], None]:
    """Создать файл с настройками.

    :param work_dir: относительный путь к папке
    :param command: команда
    :return: задача
    """

    def _task() -> None:
        log.info("Экспортируем файл с настройками")
        export_path_abs: str = dir_rel_to_abs(export_path_rel)
        log.info(f"Папка для экспорта: {export_path_abs}")
        log.info(f"Файл для экспорта: {export_filename}")
        main(
            work_dir=work_path_rel,
            command=f'{command} --path "{export_path_abs}" --filename {export_filename}',
        )()

    return _task
