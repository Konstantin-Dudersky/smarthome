#!/usr/bin/env python3
"""Скрипты для установки / обновления.

Запускаются в python3.7 и выше.

Исходный репозиторий - https://github.com/Konstantin-Dudersky/setup.

Обновить из репозитория:
git clone https://github.com/Konstantin-Dudersky/setup.git setup_clone \
&& rm -rf setup_clone/.git \
&& rsync -va setup_clone/ setup --ignore-existing \
&& rsync -va setup_clone/setup/ setup/setup \
&& rm -rf setup_clone

Использование:

- вывести список задач для выполнения:
./dev.py

- запустить задачу task_name на выполнение:
./dev.py task_name
"""

import sys
from typing import Final, NamedTuple, Set, TYPE_CHECKING

from setup import setup

if TYPE_CHECKING:
    import setup

SYSTEMD_SERVICE: str = "smarthome"
IMAGE_SETUP: str = "target:5000/inosat/kleck_setup"
BIND_SRC_FOLDER: str = "type=bind,src=`pwd`,dst=/root/code"
PARENT_FOLDER: str = "../."

PYTHON_PROJECTS: Set[str] = {
    "./db",
    "./driver_deconz",
    "./setup",
    "./shared",
}
NG_PROJECTS: Set[str] = {
    "./webapp",
}
REMOTE_USER: Final[str] = "root"
REMOTE_HOST: Final[str] = "target"
REMOTE_CODE_FOLDER: Final[str] = "/home/code"


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
    docker_install: setup.BaseTask = setup.DockerInstall()
    docker_install_remote: setup.BaseTask = setup.RemoteCommand(
        desc="Устанока Docker на целевой машине",
        command="./run.py docker_install",
        remote_user=REMOTE_USER,
        remote_host=REMOTE_HOST,
        remote_folder=REMOTE_CODE_FOLDER,
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
    docker_compose_pull_remote: setup.BaseTask = setup.RemoteCommand(
        desc="Загрузить образы docker из хранилища",
        command="docker compose --profile {profile} pull".format(
            profile="notification",
        ),
        remote_user=REMOTE_USER,
        remote_host=REMOTE_HOST,
        remote_folder=REMOTE_CODE_FOLDER,
    )
    docker_compose_up_system: setup.BaseTask = setup.RemoteCommand(
        desc="Запуск системных образов Docker",
        command="docker compose --profile system up -d",
        remote_user=REMOTE_USER,
        remote_host=REMOTE_HOST,
        remote_folder=REMOTE_CODE_FOLDER,
    )
    create_env: setup.BaseTask = setup.docker_tasks.DockerRunExecRemove(
        desc="Создать файл .env",
        image=IMAGE_SETUP,
        command="poetry run create_env",
    )
    create_env_remote: setup.BaseTask = setup.RemoteCommand(
        desc="Создать файл .env на целевой машине",
        command="./run.py create_env",
        remote_user=REMOTE_USER,
        remote_host=REMOTE_HOST,
        remote_folder=REMOTE_CODE_FOLDER,
    )
    edit_env_remote: setup.BaseTask = setup.RemoteCommand(
        desc="Редактировать файл .env на целевой машине",
        command="nano .env",
        remote_user=REMOTE_USER,
        remote_host=REMOTE_HOST,
        remote_folder=REMOTE_CODE_FOLDER,
    )
    export_env_schema: setup.BaseTask = setup.docker_tasks.DockerRunExecRemove(
        desc="Экспортировать настройки в json файл",
        image=IMAGE_SETUP,
        command="poetry run export_env_schema",
    )
    systemd_create: setup.BaseTask = setup.systemd.SystemdDockerCompose(
        desc="Создание сервиса systemd",
        profile="pi",
        work_dir_rel=".",
        service_name=SYSTEMD_SERVICE,
    )
    systemd_create_remote: setup.BaseTask = setup.RemoteCommand(
        desc="Создание сервиса systemd на целевой машине",
        command="./run.py systemd_create",
        remote_user=REMOTE_USER,
        remote_host=REMOTE_HOST,
        remote_folder=REMOTE_CODE_FOLDER,
    )


class TasksOld(NamedTuple):
    # webapp_build: setup.Task = setup.Task(
    #     desc="Сборка проекта Angular",
    #     task=setup.ng_build(
    #         work_dir_relative="../webapp",
    #         project="client",
    #         base_href="/",
    #     ),
    # )
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
    # system_share_folder: setup.Task = setup.Task(
    #     desc="Создание общей папки", task=setup.samba("../../share")
    # )
    # alembic_upgrade: setup.Task = setup.Task(
    #     desc="Обновить схему БД",
    #     task=setup.docker_tasks.run_exec_remove(
    #         work_dir_rel=PARENT_FOLDER,
    #         image=IMAGE_SETUP,
    #         mount=BIND_SRC_FOLDER,
    #         command="poetry run python main.py venv_alembic_upgrade",
    #     ),
    # )
    pass


TASKS = Tasks()


DOCKER_INSECURE: str = """
Добавить в файл `/etc/docker/daemon.json` :
sys.argv, TASKS, COMPOSE_TASKS
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
    dev_update: setup.ComposeTask = setup.ComposeTask(
        desc="Обновление зависимостей проекта",
        subtasks=[
            TASKS.poetry_update,
            TASKS.poetry_show_outdated,
            TASKS.npm_update,
            TASKS.npm_outdated,
        ],
    )
    dev_build: setup.ComposeTask = setup.ComposeTask(
        desc="Сборка проекта",
        subtasks=[
            TASKS.black,
            TASKS.pyright,
            TASKS.flake8,
            TASKS.prettier,
            TASKS.compodoc,
            TASKS.export_env_schema,
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
            TASKS.docker_install_remote,
            TASKS.docker_compose_up_system,
            TASKS.docker_move_images,
            TASKS.create_env_remote,
            TASKS.edit_env_remote,
            TASKS.docker_compose_pull_remote,
            TASKS.systemd_create_remote,
        ],
    )
    target_install_2: setup.ComposeTask = setup.ComposeTask(
        desc="Установка на целевой системе, ч.2",
        subtasks=[
            TASKS.codesync,
        ],
    )
    target_update: setup.ComposeTask = setup.ComposeTask(
        desc="Обновление проекта на целевой системе",
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
    setup.Runner(sys.argv, TASKS, COMPOSE_TASKS)
