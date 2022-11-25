"""Create systemd service file."""

import getpass
import logging
import os
from pathlib import Path
from typing import Callable

from ..internal.shared import dir_rel_to_abs

log: logging.Logger = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

SERVICE: str = """
[Unit]
Description={description}

[Service]
Restart=always
RestartSec=10s
Type=simple
User={user}
Group={user}
EnvironmentFile=/etc/environment
WorkingDirectory={work_dir}
ExecStart={poetry_bin} run python {start_file}

[Install]
WantedBy=multi-user.target"""


SERVICE_DOCKER_COMPOSE: str = """
[Unit]
Description=Docker Compose Application Service
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory={workdir}
ExecStart=docker compose --profile {profile} up -d
ExecStop=docker compose --profile {profile} down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
"""


def main(
    service_name: str,
    description: str,
    work_dir_relative: str,
    start_file: str = "start.py",
) -> Callable[[], None]:
    """Создать сервис.

    :param service_name: название сервиса
    :param description: описание сервиса
    :param work_dir_relative: относительный путь для рабочей папки сервиса
    :param start_file: файл для запуска
    """

    def _main() -> None:
        home_dir = str(Path.home())
        poetry_bin = os.path.join(home_dir, ".local", "bin", "poetry")
        print(f"-> Poetry bin path: {poetry_bin}")
        curr_dir = os.getcwd()
        work_dir_abs_full = os.path.join(curr_dir, work_dir_relative)
        work_dir_abs = os.path.abspath(work_dir_abs_full)
        print(f"-> Work dir absolute path: {work_dir_abs}")
        service = SERVICE.format(
            description=description,
            user=getpass.getuser(),
            work_dir=work_dir_abs,
            poetry_bin=poetry_bin,
            start_file=start_file,
        )
        print(f"-> Final service file: \n{service}\n")
        filename = f"src/{service_name}.service"
        with open(filename, "w", encoding="utf-8") as file:
            file.write(service)
        print(f"-> File {filename} created")
        os.system(f"sudo mv {filename} /etc/systemd/system")
        os.system("sudo systemctl daemon-reload")
        os.system(f"sudo systemctl enable {service_name}")

    return _main


def docker_compose(
    service_name: str,
    profile: str,
    work_dir_rel: str,
) -> Callable[[], None]:
    """Сервис для запуска стека контейнеров.

    :param service_name: название сервиса
    :param profile: профиль
    :param work_dir_rel: относительный путь для рабочей папки сервиса
    """

    def _task() -> None:
        log.info("Создаем сервис для запуска docker compose")
        work_dir_abs: str = dir_rel_to_abs(work_dir_rel)
        log.info("Рабочая папка с проектом: %s", work_dir_abs)
        service: str = SERVICE_DOCKER_COMPOSE.format(
            workdir=work_dir_abs,
            profile=profile,
        )
        log.info("Файл сервиса:\n%s", service)
        filename: str = "src/{0}.service".format(service_name)
        with open(filename, "w", encoding="utf-8") as file:
            file.write(service)
        os.system(f"sudo mv {filename} /etc/systemd/system")
        os.system("sudo systemctl daemon-reload")
        os.system(f"sudo systemctl enable {service_name}")

    return _task


if __name__ == "__main__":
    main(
        service_name="service",
        description="description",
        work_dir_relative="../server",
    )
