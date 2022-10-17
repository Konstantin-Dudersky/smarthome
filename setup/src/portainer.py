"""GUI для управления образами docker."""

import logging
import os
from typing import Callable

from ._shared import get_logger

log: logging.Logger = get_logger(__name__)

DOCKER_RUN: str = """
docker run -d \
-p 8000:8000 \
-p 9443:9443 \
--name portainer \
--restart=always \
-v /var/run/docker.sock:/var/run/docker.sock \
-v portainer_data:/data \
portainer/portainer-ce:latest
"""


def install() -> Callable[[], None]:
    def _task() -> None:
        log.info("Создание радела для хранения данных")
        os.system("sudo docker volume create portainer_data")
        log.info("Установка образа")
        os.system(DOCKER_RUN)
        log.info("portainer установлен, адрес: https://IP:9443")

    return _task


def update() -> Callable[[], None]:
    def _task() -> None:
        os.system("docker stop portainer")
        os.system("docker rm portainer")
        os.system("docker pull portainer/portainer-ce:latest")
        os.system(DOCKER_RUN)

    return _task
