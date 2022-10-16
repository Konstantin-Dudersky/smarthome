"""Установка TimescaleDB."""

import logging
import os
from typing import Callable

from .const import SystemVers

log: logging.Logger = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

REPO_URL: str = "https://packagecloud.io/timescale/timescaledb"
REPO_APT_RECORD: str = (
    "'deb {repo_url}/ubuntu/ $(lsb_release -c -s) main'".format(
        repo_url=REPO_URL,
    )
)
ADD_REPO: str = (
    'sudo sh -c "echo {repo_apt_record} > '
    + '/etc/apt/sources.list.d/timescaledb.list"'
).format(
    repo_apt_record=REPO_APT_RECORD,
)
ADD_REPO_KEY: str = (
    "sudo wget --quiet -O - {repo_url}/gpgkey | "
    + 'sudo sh -c "gpg --dearmor > /etc/apt/trusted.gpg.d/timescaledb.gpg"'
).format(
    repo_url=REPO_URL,
)


def install_ubuntu_2204() -> None:
    os.system(
        "sudo apt install gnupg postgresql-common apt-transport-https "
        + "lsb-release wget",
    )
    os.system("sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh")
    os.system(ADD_REPO)
    os.system(ADD_REPO_KEY)
    os.system("sudo apt update")
    os.system("sudo apt install timescaledb-2-postgresql-14")


def tune_ubuntu_2204() -> None:
    os.system("sudo apt install golang-go")
    os.system(
        "go install "
        + "github.com/timescale/timescaledb-tune/cmd/timescaledb-tune@latest",
    )
    os.system("sudo timescaledb-tune")


def install(
    system_version: SystemVers = SystemVers.ubuntu_22_04,
) -> Callable[[], None]:
    """Установка TimescaleDB в системе.

    :param system_version: версия ОС
    :return: task
    """

    def _task() -> None:
        if system_version == SystemVers.ubuntu_22_04:
            install_ubuntu_2204()

    return _task


def tune(
    system_version: SystemVers = SystemVers.ubuntu_22_04,
) -> Callable[[], None]:
    """Тюнинг параметров производительности TimescaleDB.

    :param system_version: версия ОС
    :return: task
    """

    def _task() -> None:
        if system_version == SystemVers.ubuntu_22_04:
            tune_ubuntu_2204()

    return _task
