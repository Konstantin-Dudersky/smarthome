#!/usr/bin/env python3
"""Скрипты для установки / обновления.

Запускаются в python3.7 и выше.

Исходный репозиторий - https://github.com/Konstantin-Dudersky/setup.

Обновить из репозитория:
git clone https://github.com/Konstantin-Dudersky/setup.git setup_clone \
&& rm -rf setup_clone/.git \
&& rsync -va setup_clone/ setup \
&& rm -rf setup_clone

Использование:

- вывести список задач для выполнения:
./dev.py

- запустить задачу task_name на выполнение:
./dev.py task_name
"""

import sys
from typing import NamedTuple, Set


from setup import setup

SYSTEMD_SERVICE: str = "kleck"
IMAGE_SETUP: str = "target:5000/inosat/kleck_setup"
BIND_SRC_FOLDER: str = "type=bind,src=`pwd`,dst=/root/code"
PARENT_FOLDER: str = "../."


PYTHON_PROJECTS: Set[str] = {
    "./db",
    "./driver_deconz",
    "./shared",
}
NG_PROJECTS: Set[str] = {
    "./webapp",
}


def is_venv() -> bool:
    """Проверяем, что модуль запущен в виртуальном окружении.

    Returns
    -------
    bool
        True - в виртуальном окружении
    """
    is_real_prefix: bool = hasattr(sys, "real_prefix")  # noqa: WPS421
    is_base_prefix: bool = (
        hasattr(sys, "base_prefix") and sys.base_prefix != sys.prefix  # noqa: WPS421
    )
    return is_real_prefix or is_base_prefix


class Tasks(NamedTuple):
    add_permissions_for_serial: setup.BaseTask = setup.SimpleCommand(
        desc="Разрешение на использование порта",
        command=r"sudo gpasswd --add ${USER} dialout",
    )
    reboot: setup.BaseTask = setup.SimpleCommand(
        desc="Перезагрузка",
        command="sudo reboot",
    )
    codesync: setup.BaseTask = setup.CodeSync(
        desc="Синхронизация кода с целевой системой",
        remote_path="admin@target:/home/admin/code",
    )
    poetry_install: setup.BaseTask = setup.SimpleCommandMultifolder(
        desc="Установка виртуальных окружений python",
        dirs=PYTHON_PROJECTS,
        command="poetry install",
    )
    poetry_remove: setup.BaseTask = setup.SimpleCommandMultifolder(
        desc="Удаление виртуальных окружений python",
        dirs=PYTHON_PROJECTS,
        command="poetry env remove --all",
    )
    poetry_update: setup.BaseTask = setup.SimpleCommandMultifolder(
        desc="Обновление виртуальных окружений python",
        dirs=PYTHON_PROJECTS,
        command="poetry update",
    )
    poetry_show_outdated: setup.BaseTask = setup.SimpleCommandMultifolder(
        desc="Проверка устаревших пакетов python",
        dirs=PYTHON_PROJECTS,
        command="poetry show -o",
    )
    pyright: setup.BaseTask = setup.SimpleCommandMultifolder(
        desc="Проверка pyright",
        command="pyright",
        dirs=PYTHON_PROJECTS,
    )
    flake8: setup.BaseTask = setup.SimpleCommandMultifolder(
        desc="Проверка исходников через flake8",
        command="poetry run flake8",
        dirs=PYTHON_PROJECTS,
    )
    black: setup.BaseTask = setup.SimpleCommandMultifolder(
        desc="Форматирование исходников через black",
        command="poetry run black .",
        dirs=PYTHON_PROJECTS,
    )
    npm_install: setup.BaseTask = setup.SimpleCommandMultifolder(
        desc="Установка пакетов npm",
        command="npm install",
        dirs=NG_PROJECTS,
    )
    npm_update: setup.BaseTask = setup.SimpleCommandMultifolder(
        desc="Обновление пакетов npm",
        command="npm update",
        dirs=NG_PROJECTS,
    )
    npm_remove: setup.BaseTask = setup.SimpleCommandMultifolder(
        desc="Удаление пакетов npm",
        command="rm -rf node_modules",
        dirs=NG_PROJECTS,
    )
    npm_outdated: setup.BaseTask = setup.SimpleCommandMultifolder(
        desc="Проверка устаревших пакетов npm",
        command="npm outdated",
        dirs=NG_PROJECTS,
    )
    prettier: setup.BaseTask = setup.SimpleCommandMultifolder(
        desc="Форматирование исходников веб-приложения",
        dirs=NG_PROJECTS,
        command="npx prettier --write src",
    )
    compodoc: setup.BaseTask = setup.SimpleCommandMultifolder(
        desc="Документация веб-приложения",
        command="npm run compodoc",
        dirs=NG_PROJECTS,
    )
    docker_build_images: setup.BaseTask = setup.SimpleCommand(
        desc="Сборка образов docker",
        command="docker buildx bake --builder builder -f docker-bake.hcl --push pi",
    )
    docker_move_images: setup.BaseTask = setup.DockerMoveImages(
        profile="pi",
        repo_from="localhost:5000",
        repo_to="target:5000",
        arch="linux/arm64",
    )


class TasksOld(NamedTuple):
    # docker_compose_system: setup.Task = setup.Task(
    #     desc="Запустить системные сервисы",
    #     task=setup.cmd_in_dir(
    #         work_dir="../.",
    #         command="docker compose -f docker-compose.system.yml up -d",
    #     ),
    # )

    webapp_build: setup.Task = setup.Task(
        desc="Сборка проекта Angular",
        task=setup.ng_build(
            work_dir_relative="../webapp",
            project="client",
            base_href="/",
        ),
    )
    docker_install: setup.Task = setup.Task(
        desc="Установка docker",
        task=setup.docker_tasks.install(),
    )
    # docker_compose_pull: setup.Task = setup.Task(
    #     desc="Скачать образы из dockerhub",
    #     task=setup.cmd_in_dir(
    #         work_dir="../.",
    #         command="docker compose --profile server pull",
    #     ),
    # )
    create_env: setup.Task = setup.Task(
        desc="Создать файл .env с настройками",
        task=setup.docker_tasks.run_exec_remove(
            work_dir_rel=PARENT_FOLDER,
            image=IMAGE_SETUP,
            mount=BIND_SRC_FOLDER,
            command="poetry run python main.py venv_create_env",
        ),
    )
    # server_export_openapi: setup.Task = setup.Task(
    #     desc="Экспорт спецификации API",
    #     task=setup.cmd_in_dir(
    #         work_dir="../server",
    #         command="poetry run poe export_openapi",
    #     ),
    # )
    # server_service_start: setup.Task = setup.Task(
    #     desc="Запустить сервис",
    #     task=setup.cmd_in_dir(
    #         work_dir=".", command=f"sudo systemctl start {SYSTEMD_SERVICE}"
    #     ),
    # )
    # server_service_stop: setup.Task = setup.Task(
    #     desc="Остановить сервис",
    #     task=setup.cmd_in_dir(
    #         work_dir=".", command=f"sudo systemctl stop {SYSTEMD_SERVICE}"
    #     ),
    # )
    system_share_folder: setup.Task = setup.Task(
        desc="Создание общей папки", task=setup.samba("../../share")
    )
    server_systemd_create: setup.Task = setup.Task(
        desc="Создание сервиса systemd",
        task=setup.systemd.docker_compose(
            service_name=SYSTEMD_SERVICE,
            profile="server",
            work_dir_rel="../.",
        ),
    )
    alembic_upgrade: setup.Task = setup.Task(
        desc="Обновить схему БД",
        task=setup.docker_tasks.run_exec_remove(
            work_dir_rel=PARENT_FOLDER,
            image=IMAGE_SETUP,
            mount=BIND_SRC_FOLDER,
            command="poetry run python main.py venv_alembic_upgrade",
        ),
    )


TASKS = Tasks()


if is_venv():
    from alembic import config as alembic_config

    # from server import utils  # noqa: WPS433
    from server.utils import settings

    class TasksEnv(NamedTuple):
        """Перечень задач.

        Могут выполняться только в установленном виртуальном окружении.
        """

        venv_create_env: setup.Task = setup.Task(
            desc="Создать файл .env с настройками",
            task=setup.call_func.call_func(
                work_dir_rel=".",
                func=lambda: settings.create_env(),
            ),
            confirm=False,
        )
        venv_alembic_upgrade: setup.Task = setup.Task(
            desc="Обновить схему БД",
            task=setup.call_func.call_func(
                work_dir_rel="../server",
                func=lambda: alembic_config.main(argv=["upgrade", "head"]),
            ),
            confirm=False,
        )

    tasks_env = TasksEnv()
else:
    tasks_env = None


DOCKER_INSECURE: str = """
Добавить в файл `/etc/docker/daemon.json` :

$ sudo nano /etc/docker/daemon.json

строку:

{ "insecure-registries":["target:5000"] }

И перезагрузить сервис:

sudo systemctl restart docker
"""


class ComposeTasks(NamedTuple):
    dev_prepare: setup.ComposeTask = setup.ComposeTask(
        desc="Подготовка dev системы",
        subtasks=[
            TASKS.poetry_install,
            TASKS.npm_install,
        ],
    )
    dev_build: setup.ComposeTask = setup.ComposeTask(
        desc="Сборка проекта",
        subtasks=[
            TASKS.poetry_update,
            TASKS.poetry_show_outdated,
            TASKS.black,
            TASKS.pyright,
            TASKS.flake8,
            TASKS.npm_update,
            TASKS.npm_outdated,
            TASKS.prettier,
            TASKS.compodoc,
            TASKS.docker_build_images,
        ],
    )
    dev_clear: setup.ComposeTask = setup.ComposeTask(
        desc="Очистка dev системы",
        subtasks=[
            TASKS.poetry_remove,
            TASKS.npm_remove,
        ],
    )
    target_install_1: setup.ComposeTask = setup.ComposeTask(
        desc="Установка на целевой системе, ч.1",
        subtasks=[
            TASKS.codesync,
        ],
    )
    target_install_2: setup.ComposeTask = setup.ComposeTask(
        desc="Установка на целевой системе, ч.2",
        subtasks=[
            TASKS.codesync,
            TASKS.docker_move_images,
        ],
    )

    # build: setup.ComposeTask = setup.ComposeTask(
    #     desc="Сборка проекта",
    #     subtasks=[
    #         TASKS.webapp_build,
    #         TASKS.server_export_openapi,
    #     ],
    # )
    # install_1: setup.ComposeTask = setup.ComposeTask(
    #     desc="Первоначальная установка проекта на целевой системе, ч.1",
    #     subtasks=[
    #         TASKS.add_permissions_for_serial,
    #         TASKS.docker_install,
    #         setup.Task(
    #             desc="",
    #             confirm=False,
    #             task=setup.user_intercation.confirm(DOCKER_INSECURE),
    #         ),
    #         TASKS.reboot,
    #     ],
    # )
    # install_2: setup.ComposeTask = setup.ComposeTask(
    #     desc="Первоначальная установка проекта на целевой системе, ч.2",
    #     subtasks=[
    #         TASKS.create_env,
    #         TASKS.alembic_upgrade,
    #         TASKS.server_systemd_create,
    #         TASKS.server_service_start,
    #     ],
    # )
    # update: setup.ComposeTask = setup.ComposeTask(
    #     desc="Обновить проект на целевой системе",
    #     subtasks=[
    #         TASKS.server_service_stop,
    #         TASKS.docker_compose_pull,
    #         TASKS.alembic_upgrade,
    #         TASKS.server_service_start,
    #     ],
    # )


COMPOSE_TASKS = ComposeTasks()


if __name__ == "__main__":
    setup.execute(sys.argv, TASKS, tasks_env, COMPOSE_TASKS)
