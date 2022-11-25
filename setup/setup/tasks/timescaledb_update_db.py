#!/usr/bin/env python3
"""Обновить базу данных для TimescaleDB."""

import os
from typing import Callable


CMD: str = """echo "CREATE EXTENSION IF NOT EXISTS timescaledb;\\gexec" | sudo -u postgres psql -d {db_name}
"""


def main(db_name: str) -> Callable[[], None]:
    """Entry point."""

    def _main() -> None:
        print(f"-> Обновить базу данных {db_name} для TimescaleDB")
        os.system("sudo systemctl restart postgresql")
        os.system(CMD.format(db_name=db_name))

    return _main
