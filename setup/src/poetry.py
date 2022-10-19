"""Установка poetry."""

import logging
import os
import subprocess  # noqa: S404
from pathlib import Path
from typing import Callable

from ._shared import get_logger, dir_rel_to_abs

log = get_logger(__name__, logging.DEBUG)

POETRY_BIN: str = "~/.local/share/pypoetry/venv/bin/poetry"


def self_install(version: str = "1.2.0") -> Callable[[], None]:
    """Установить в системе poerty.

    :param version: версия для установки
    :return: функция
    """

    def _main() -> None:
        log.info("Версия poetry в системе:")
        os.system("poetry --version")
        while True:
            log.info("-> Установить ? (y/n)")
            ans = input()
            if ans == "y":
                break
            elif ans == "n":
                return
        os.system(
            "sudo apt install -y python3-venv curl python3-dev build-essential"
        )
        os.system(
            "curl -sSL https://install.python-poetry.org"
            f" | python3 - --version {version}",
        )
        os.system(f"{POETRY_BIN} config virtualenvs.in-project true")

    return _main


def self_update(version: str = "1.2.0") -> Callable[[], None]:
    """Обновить poetry.

    :param version: версия для обновления
    :return: задача
    """

    def _main() -> None:
        log.info("Версия poetry в системе:")
        os.system("poetry --version")
        while True:
            log.info("-> Обновить ? (y/n)")
            ans = input()
            if ans == "y":
                break
            elif ans == "n":
                return
        os.system(f"poetry self update {version}")

    return _main


def check_version() -> Callable[[], None]:
    """Проверка, что poetry установлена.

    :return: задача
    """

    def _main() -> None:
        log.info("Версия poetry в системе:")
        os.system("poetry --version")
        log.warning(
            "Если версия poetry не найдена, необходимо "
            "добавить в файл ~/.bashrc:",
        )
        log.warning('\nexport PATH="$HOME/.local/bin:$PATH"')
        log.warning(
            "\nПосле перезапустить систему и "
            "продолжить установку с этого шага",
        )

    return _main


def show_outdated(work_path_rel: str) -> Callable[[], None]:
    """Проверка устаревших пакетов.

    :return: задача
    """

    def _main() -> None:
        work_path_abs = dir_rel_to_abs(work_path_rel)
        log.info("Проверка пакетов в папке: %s", work_path_abs)
        os.chdir(work_path_abs)
        log.info("Устаревшие пакеты:")
        os.system("poetry show -o")

    return _main


def update_lock_and_show_outdated(
    dirs: list[str] | None = None,
) -> Callable[[], None]:
    """Обновить lock файл и вывести список устаревших пакетов.

    Parameters
    ----------
    dirs
        Перечень относительных путей к папкам

    Returns
    -------
    Задача для выполнения
    """

    def _task() -> None:
        cwd = Path.cwd()
        for dir_rel in dirs:
            dir_abs: str = Path(dir_rel).resolve().as_posix()
            log.info("Папка: {0}".format(dir_abs))
            os.chdir(dir_abs)
            log.info("Обновим файл lock в {0}".format(dir_rel))
            subprocess.run("poetry update --lock".split())  # noqa: S603
            log.info("Перечень устаревших пакетов в {0}:".format(dir_rel))
            subprocess.run("poetry show -o".split())  # noqa: S603
            os.chdir(cwd)

    return _task
