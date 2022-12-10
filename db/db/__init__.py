"""Подключение к БД db_conf, db_data."""

from . import conf, data
from .connection_string import ConnectionString

__all__: list[str] = [
    "conf",
    "data",
    "ConnectionString",
]
