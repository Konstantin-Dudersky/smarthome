"""БД db_data."""

from . import timescaledb
from .database import Database

__all__: list[str] = [
    "Database",
    "timescaledb",
]
