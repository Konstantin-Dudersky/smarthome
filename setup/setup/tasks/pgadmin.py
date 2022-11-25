"""Установка pgAdmin.

Описание - https://www.pgadmin.org/download/pgadmin-4-apt/
"""

import os
from typing import Callable


def main() -> Callable[[], None]:
    """Entry point."""

    def _main() -> None:
        print("-> Установка pgAdmin")
        os.system(
            "sudo wget -q -O - https://www.pgadmin.org/static/packages_pgadmin_org.pub | sudo apt-key add"
        )
        os.system(
            """sudo sh -c 'echo "deb https://ftp.postgresql.org/pub/pgadmin/pgadmin4/apt/$(lsb_release -cs) pgadmin4 main" > /etc/apt/sources.list.d/pgadmin4.list && apt update'
        """
        )
        os.system("sudo apt install pgadmin4-web")
        os.system("sudo /usr/pgadmin4/bin/setup-web.sh")

    return _main
