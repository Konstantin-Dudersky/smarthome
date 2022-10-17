"""Работа с проектом Angular."""

import logging
import os
from typing import Callable

from ._shared import dir_rel_to_abs

log: logging.Logger = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def build(
    project_dir_rel: str = "../webapp",
    target_dir_rel: str = "../../dist",
    project: str = "client",
    base_href: str = "/",
) -> Callable[[], None]:
    """Сборка проекта.

    :param project_dir_rel: относительный путь к папке с проектом
    :param target_dir_rel: относительный путь к папке с проектом
    :param project: название проекта
    :param base_href: начальная часть всех ссылок, параметр при сборке
    :return: задача
    """

    def _task() -> None:
        project_dir_abs: str = dir_rel_to_abs(project_dir_rel)
        target_dir_abs: str = dir_rel_to_abs(target_dir_rel)
        log.info("Папка с проектом: %s", project_dir_abs)
        os.chdir(project_dir_abs)
        os.system(f"ng build --base-href {base_href}")
        filename: str = f"dist/{project}.zip"
        os.system(f"zip -j -r {filename} dist/{project}/")
        os.system(f"rm -rf dist/{project}/")
        log.info("Создан архив: %s", filename)
        os.system(f"mv {filename} {target_dir_abs}")
        log.info("Архив перемещен в папку %s", target_dir_abs)

    return _task


def dist(
    source_dir_rel: str = "../client/",
    target_dir_rel: str = "../server/static/",
    project: str = "client",
) -> Callable[[], None]:
    """
    Разворачивание проекта.

    :param source_dir_rel: относительный путь к папке с архивом
    :param target_dir_rel: относительный путь к целевой папке
    :param project: _description_, defaults to "client"
    :return: задача
    """

    def _task() -> None:
        os.system("sudo apt install -y unzip")
        curr_dir = os.getcwd()
        source_file = os.path.abspath(
            os.path.join(curr_dir, source_dir_rel, project + ".zip"),
        )
        log.info(f"-> Исходный файл: {source_file}")
        target_dir = os.path.abspath(os.path.join(curr_dir, target_dir_rel))
        log.info(f"-> Целевая папка: {target_dir}")
        os.system(f"unzip -uo {source_file} -d {target_dir}")

    return _task
