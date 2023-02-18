"""Установка Docker."""

import logging
import os

from ..internal.base_task import BaseTask

_log = logging.getLogger(__name__)
_log.setLevel(logging.DEBUG)


class DockerInstall(BaseTask):
    """Установка Docker."""

    def __init__(
        self,
        desc: str = "Установка Docker",
        need_confirm: bool = True,
    ) -> None:
        """Установка Docker."""
        super().__init__(desc, need_confirm)

    def _execute(self) -> None:
        os.system("sudo apt install -y curl")
        _log.info("Устанавливаем Docker")
        os.system("curl -fsSL https://get.docker.com -o get-docker.sh")
        os.system("sudo sh get-docker.sh")
        _log.info("Проверим, что docker установился корректно")
        os.system("sudo docker run --name hello-world hello-world")
        os.system("sudo groupadd docker")
        os.system("sudo usermod -aG docker $USER")
