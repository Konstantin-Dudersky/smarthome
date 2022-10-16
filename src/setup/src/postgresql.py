"""Установка PostgreSQL.

user:password - postgres:postgres
"""

import logging
import os
from typing import Callable

from ._shared import wait_confirmation

log: logging.Logger = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

INSTALL: str = "sudo apt install postgresql-14 libpq-dev"

ALTER_PASSWD: str = """
echo "ALTER USER postgres PASSWORD 'postgres';" | sudo -u postgres psql"""

POSTGRESQL_CONF: str = "/etc/postgresql/14/main/postgresql.conf"
POSTGRESQL_CONF_DATA: str = 'listen_addresses = " * "'

PG_HBA_CONF: str = "/etc/postgresql/14/main/pg_hba.conf"
PG_HBA_CONF_DATA: str = """
host    all             all              0.0.0.0/0                       md5
host    all             all              ::/0                            md5
"""


def install(system_version: str = "ubuntu-22.04") -> Callable[[], None]:
    """Entry point.

    :param system_version: версия ОС
    :return: задача
    """

    def _main() -> None:
        if system_version == "ubuntu-22.04":
            log.info("Установка PostgreSQL v14")
            os.system(INSTALL)
            os.system(ALTER_PASSWD)
            log.info(
                "postgresql установлена, необходимо открыть доступ по сети",
            )
            log.info("Открой файл\n%s\nи задай:", POSTGRESQL_CONF)
            log.info(POSTGRESQL_CONF_DATA)
            wait_confirmation()
            log.info("Открой файл\n%s\nи добавь:", PG_HBA_CONF)
            log.info(PG_HBA_CONF_DATA)
            wait_confirmation()
            os.system("sudo systemctl restart postgresql.service")
            log.warning("\nПользователь и пароль по-умолчанию:")
            log.warning("postgres:postgres")
            wait_confirmation()

    return _main


if __name__ == "__main__":
    install()
