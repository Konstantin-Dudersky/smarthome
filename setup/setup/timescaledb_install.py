#!/usr/bin/env python3
"""Установка TimescaleDB."""

import os
from typing import Callable


def ubuntu_2204():
    print("-> Установка базы данных TimescaleDB")
    os.system(
        "sudo apt install gnupg postgresql-common apt-transport-https lsb-release wget"
    )
    os.system("sudo /usr/share/postgresql-common/pgdg/apt.postgresql.org.sh")
    os.system(
        """sudo sh -c "echo 'deb https://packagecloud.io/timescale/timescaledb/ubuntu/ $(lsb_release -c -s) main' > /etc/apt/sources.list.d/timescaledb.list"
    """
    )
    os.system(
        """sudo wget --quiet -O - https://packagecloud.io/timescale/timescaledb/gpgkey | sudo sh -c "gpg --dearmor > /etc/apt/trusted.gpg.d/timescaledb.gpg"
    """
    )
    os.system("sudo apt update")
    os.system("sudo apt install timescaledb-2-postgresql-14")
    print("-> TimescaleDB tuning tool")
    os.system("sudo apt install golang-go")
    os.system(
        "go install github.com/timescale/timescaledb-tune/cmd/timescaledb-tune@latest"
    )
    os.system("sudo timescaledb-tune")


def main(system_version: str = "ubuntu-22.04") -> Callable[[], None]:
    """Entry point."""

    def _main() -> None:
        if system_version == "ubuntu-22.04":
            ubuntu_2204()

    return _main
