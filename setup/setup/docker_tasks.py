"""Задачи docker."""

# pyright: reportUnknownMemberType=false
# pyright: reportGeneralTypeIssues=false

import logging
import os
from typing import Callable, List, Literal, Optional

from ._shared import dir_rel_to_abs, get_logger


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


def _output_build(stream: List[str]) -> None:
    for item in stream[1]:
        for key, value in item.items():
            if key == "stream":
                text: str = value.strip()
                if text:
                    print(text)


def build(
    work_path_rel: str = "../server",
    dockerfile: str = "Dockerfile",
    name: str = "inosat/image",
    tag: str = "latest",
    platform: platforms = "linux/amd64",
) -> Callable[[], None]:
    """Собрать образ."""

    def _task() -> None:
        work_path_abs: str = dir_rel_to_abs(work_path_rel)
        os.chdir(work_path_abs)
        client: docker.client.DockerClient = docker.from_env()
        result = client.images.build(
            path=".",
            dockerfile=dockerfile,
            tag=f"{name}:{tag}",
            platform=platform,
            forcerm=True,
            network_mode="host",
            pull=True,
        )
        _output_build(result)
        log.info("{name} собран".format(name=name))

    return _task


def push(
    name: str = "inosat/image",
) -> None:
    client: docker.client.DockerClient = docker.from_env()
    line: str
    for line in client.images.push(name, stream=True, decode=True):
        log.debug(line)
    log.info("{name} опубликован".format(name=name))


def build_and_push(
    work_path_rel: str = "../server",
    dockerfile: str = "Dockerfile",
    name: str = "inosat/image",
    tag: str = "latest",
    platform: platforms = "linux/amd64",
) -> Callable[[], None]:
    """Собрать образ."""

    def _task() -> None:
        build(
            work_path_rel=work_path_rel,
            dockerfile=dockerfile,
            name=name,
            tag=tag,
            platform=platform,
        )()
        push(name)

    return _task


def exec_in_container(
    container: str,
    command: str,
) -> Callable[[], None]:
    """Выполнить команду в контейнере."""

    def _task() -> None:
        os.system(f"docker exec {container} {command}")

    return _task


def start_exec_in_container(
    container: str,
    command: str,
) -> Callable[[], None]:
    """Выполнить команду в контейнере."""

    def _task() -> None:
        log.info("start container: %s", container)
        os.system(f"docker container start {container}")
        exec_in_container(container, command)()
        log.info("stop container: %s", container)
        os.system(f"docker container stop {container}")

    return _task


TEMPL: str = "docker run --rm --pull always {mount} {image} {command}"


def run_exec_remove(
    work_dir_rel: str = "../server",
    image: str = "image",
    mount: Optional[str] = "type=bind,src=`pwd`,dst=/home/projects/coca/code",
    command: str = "ls -la",
) -> Callable[[], None]:
    def _task() -> None:
        curr_dir: str = os.getcwd()
        work_dir_abs = dir_rel_to_abs(work_dir_rel)
        log.info("Рабочая папка: %s", work_dir_abs)
        os.chdir(work_dir_abs)
        if mount is None:
            mount_str: str = ""
        else:
            mount_str: str = "--mount {0}".format(mount)
        os.system(
            TEMPL.format(
                mount=mount_str,
                image=image,
                command=command,
            ),
        )
        os.chdir(curr_dir)

    return _task
