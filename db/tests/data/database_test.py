import asyncio

from pydantic import BaseModel

from db.data import Database
from db import ConnectionString


class Test(BaseModel):
    test_bool: bool


def test_database(conn_str: ConnectionString) -> None:
    db = Database(conn_str=conn_str)

    async def run():
        async with db.create_session(Test):
            print("123")

    asyncio.run(run())
    assert True
