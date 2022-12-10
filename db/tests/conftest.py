import pytest

import db
from db import ConnectionString

from shared.settings import SettingsStore

settings = SettingsStore("../.env").settings


@pytest.fixture
def conn_str() -> ConnectionString:
    return ConnectionString(
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        database="db_data_test",
    )


@pytest.fixture
def database(conn_str: ConnectionString) -> db.data.Database:
    return db.data.Database(conn_str=conn_str)
