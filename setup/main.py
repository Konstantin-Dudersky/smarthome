#!/usr/bin/env python3
"""Скрипты установки."""

import sys
from typing import NamedTuple

import src


def is_venv() -> bool:
    """Проверяем, что модуль запущен в виртуальном окружении.

    Returns
    -------
    bool
        True - в виртуальном окружении
    """
    is_real_prefix: bool = hasattr(sys, "real_prefix")  # noqa: WPS421
    is_base_prefix: bool = (
        hasattr(sys, "base_prefix")  # noqa: WPS421
        and sys.base_prefix != sys.prefix
    )
    return is_real_prefix or is_base_prefix


SYSTEMD_SERVICE = "smarthome"

IMAGE_SETUP: str = "konstantindudersky/sh_setup"
BIND_SRC_FOLDER: str = "type=bind,src=`pwd`,dst=/root/code"
PARENT_FOLDER: str = "../."


class Tasks(NamedTuple):
    """Перечень задач.

    Могут выполняться напрямую из системного питона.
    """

    apt_update_upgrade: src.Task = src.Task(
        desc="Обновление системы",
        task=src.simple_command.execute(
            command="sudo apt update && sudo apt upgrade",
        ),
    )
    docker_build_images: src.Task = src.Task(
        desc="Собрать образы docker",
        task=src.cmd_in_dir(
            work_dir="../.",
            command="docker buildx bake --builder builder -f docker-bake.hcl --push pi",
        ),
    )
    docker_compose_push: src.Task = src.Task(
        desc="Опубликовать образы docker",
        task=src.cmd_in_dir(
            work_dir=PARENT_FOLDER,
            command="docker compose --profile server --profile setup push",
        ),
    )
    docker_install: src.Task = src.Task(
        desc="Установка docker",
        task=src.docker_tasks.install_raspbian(),
    )
    db_alembic_upgrade: src.Task = src.Task(
        desc="Обновить схему БД",
        task=src.docker_tasks.run_exec_remove(
            work_dir_rel=PARENT_FOLDER,
            image=IMAGE_SETUP,
            mount=BIND_SRC_FOLDER,
            command="poetry run python main.py venv_db_alembic_upgrade",
        ),
    )
    pi_create_env: src.Task = src.Task(
        desc="Создать файл .env с настройками",
        task=src.docker_tasks.run_exec_remove(
            work_dir_rel=PARENT_FOLDER,
            image=IMAGE_SETUP,
            mount=BIND_SRC_FOLDER,
            command="poetry run python main.py venv_pi_create_env",
        ),
    )
    portainer_install: src.Task = src.Task(
        desc="Установить portainer для мониторинга docker",
        task=src.portainer.install(),
    )
    update_lock_and_show_outdated: src.Task = src.Task(
        desc="Обновить пакеты poetry",
        task=src.poetry.update_lock_and_show_outdated(
            dirs=[
                "../db",
                "../docs",
                "../driver_deconz",
                "../setup",
                "../shared",
            ],
        ),
    )

    # old ----------------------------------------------------------------------

    client_ng_build: src.Task = src.Task(
        desc="Сборка проекта Angular",
        task=src.ng.build(
            project_dir_rel="../client",
            target_dir_rel=".",
            project="client",
        ),
    )
    client_ng_dist: src.Task = src.Task(
        desc="Распаковать файлы фронтенда",
        task=src.ng.dist(
            source_dir_rel="../client",
            target_dir_rel="../server/static",
            project="client",
        ),
    )
    client_tauri_build: src.Task = src.Task(
        desc="Сборка tauri",
        task=src.tauri_build(
            work_dir_relative="../client",
            project="client",
        ),
    )
    git_sync: src.Task = src.Task(
        desc="Синхронизировать проект через git",
        task=src.git_sync(),
    )
    server_lint: src.Task = src.Task(
        desc="linting",
        task=src.cmd_in_dir(
            work_dir="../server",
            command="poetry run poe lint",
        ),
    )
    server_service_start: src.Task = src.Task(
        desc="Запустить сервис",
        task=src.cmd_in_dir(
            work_dir=".",
            command=f"sudo systemctl start {SYSTEMD_SERVICE}",
        ),
    )
    server_service_stop: src.Task = src.Task(
        desc="Остановить сервис",
        task=src.cmd_in_dir(
            work_dir=".",
            command=f"sudo systemctl stop {SYSTEMD_SERVICE}",
        ),
    )
    server_share_folder: src.Task = src.Task(
        desc="Создание общей папки",
        task=src.samba("../../share"),
    )


TASKS = Tasks()


if is_venv():
    from alembic import config as alembic_config

    from shared import settings  # noqa: WPS433

    class TasksEnv(NamedTuple):
        """Перечень задач.

        Могут выполняться только в установленном виртуальном окружении.
        """

        venv_pi_create_env: src.Task = src.Task(
            desc="Создать файл .env с настройками",
            task=src.call_func.call_func(
                work_dir_rel=".",
                func=lambda: settings.create_env(
                    profiles={
                        settings.Prof.deconz_hub,
                        settings.Prof.db,
                        settings.Prof.pgadmin,
                        settings.Prof.driver_deconz,
                    },
                ),
            ),
            confirm=False,
        )
        venv_db_alembic_upgrade: src.Task = src.Task(
            desc="Обновить схему БД",
            task=src.call_func.call_func(
                work_dir_rel="../db",
                func=lambda: alembic_config.main(argv=["upgrade", "head"]),
            ),
            confirm=False,
        )

    tasks_env = TasksEnv()
else:
    tasks_env = None


class ComposeTasks(NamedTuple):
    """Сборные задачи, состоят из простых задач."""

    build: src.ComposeTask = src.ComposeTask(
        desc="Сборка проекта",
        subtasks=[
            TASKS.update_lock_and_show_outdated,
            TASKS.docker_build_images,
        ],
    )
    install: src.ComposeTask = src.ComposeTask(
        desc="Установка проекта на целевой системе",
        subtasks=[
            TASKS.apt_update_upgrade,
            TASKS.docker_install,
            TASKS.portainer_install,
            TASKS.pi_create_env,
        ],
    )
    update: src.ComposeTask = src.ComposeTask(
        desc="Обновить проект на целевой системе",
        subtasks=[
            TASKS.server_service_stop,
            TASKS.git_sync,
            TASKS.client_ng_dist,
            # TASKS.server_alembic_upgrade,
            TASKS.server_service_start,
        ],
    )


COMPOSE_TASKS = ComposeTasks()


if __name__ == "__main__":
    src.execute(sys.argv, TASKS, tasks_env, COMPOSE_TASKS)
