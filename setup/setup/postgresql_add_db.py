#!/usr/bin/env python3
"""Создать БД в postgresql если не существует."""

import os
from typing import Callable

CMD: str = """echo "SELECT 'CREATE DATABASE {db_name}' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '{db_name}')\\gexec" | sudo -u postgres psql
"""


def main(db_name: str) -> Callable[[], None]:
    """Entry point."""

    def _main() -> None:
        print(f"-> Создание БД {db_name}")
        os.system(CMD.format(db_name=db_name))

    return _main
