"""Задачи docker."""

# pyright: reportUnknownMemberType=false
# pyright: reportGeneralTypeIssues=false

import logging
import os
from typing import Callable, Literal

from ..internal.shared import get_logger
from ..internal.base_task import BaseTask


log = get_logger(__name__, logging.DEBUG)

platforms = Literal["linux/amd64"]


def install_ubuntu() -> Callable[[], None]:
    """Собрать образ."""

    def _task() -> None:
        log.info("Установка зависимостей")
        os.system("sudo apt-get install ca-certificates curl gnupg lsb-release")
        log.info("Добавление GPG ключа репозитория")
        os.system("sudo mkdir -p /etc/apt/keyrings")
        os.system(
            "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg"
        )
        log.info("Добавление репозитория")
        os.system(
            'echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null'
        )
        log.info("Установка docker engine")
        os.system("sudo apt-get update")
        os.system(
            "sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin"
        )
        log.info("Проверим, что docker установился корректно")
        os.system("sudo service docker start")
        os.system("sudo docker run --name hello-world hello-world")

    return _task


def install() -> Callable[[], None]:
    """Установить на Debian.

    Returns:
    --------
    Задача для выполнения
    """

    def _task() -> None:
        os.system("sudo apt install -y curl")
        log.info("Устанавливаем Docker")
        os.system("curl -fsSL https://get.docker.com -o get-docker.sh")
        os.system("sudo sh get-docker.sh")
        log.info("Проверим, что docker установился корректно")
        os.system("sudo docker run --name hello-world hello-world")
        os.system("sudo groupadd docker")
        os.system("sudo usermod -aG docker $USER")

    return _task


TEMPL: str = "docker run --rm -w {work_dir} --pull always --mount {mount} {image} {command}"


class DockerRunExecRemove(BaseTask):
    """Создать контейнер, выполнить команду и удалить контейнер."""

    def __init__(
        self,
        desc: str,
        need_confirm: bool = True,
        mount: str = "type=bind,src=`pwd`,dst=/root/code",
        image: str = "target:5000/smarthome/sh_setup",
        command: str = "poetry run create_env",
        work_dir: str = "/root/code/setup",
    ) -> None:
        super().__init__(desc, need_confirm)
        self.__mount = mount
        self.__image = image
        self.__command = command
        self.__work_dir = work_dir

    def _execute(self) -> None:
        os.system(
            TEMPL.format(
                mount=self.__mount,
                image=self.__image,
                command=self.__command,
                work_dir=self.__work_dir,
            ),
        )
