import asyncio

from pydantic import BaseModel

from db.data.session import Session
from db import ConnectionString


class Test(BaseModel):
    test_bool: bool


def test_connection(conn_str: ConnectionString) -> None:
    conn_str_: ConnectionString = conn_str
    conn_str_.driver = "postgresql"
    conn_str_.database = "db_data"

    async def conn():
        async with Session(conn_str_.url, Test):
            pass

    asyncio.run(conn())

    assert True
