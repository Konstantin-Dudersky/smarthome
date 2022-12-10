# pyright: reportUnknownMemberType=false

from typing import Final

from psycopg import AsyncConnection, AsyncCursor

from .models import Row

CREATE: Final[
    str
] = """
INSERT INTO {table}
VALUES {values}
ON CONFLICT (ts, entity, attr, agg) DO UPDATE
    SET value = excluded.value;
"""

READ_ALL: Final[str] = "SELECT * FROM {table}"

DELETE_ALL: Final[str] = "DELETE FROM {table}"


class CrudRows(object):
    def __init__(self, db: AsyncConnection[Row], table: str) -> None:
        self.__db: AsyncConnection[Row]
        self.__table: str

        self.__db = db
        self.__table = table

    async def create_one(self, row: Row) -> None:
        await self.__db.execute(
            query=CREATE.format(
                table=self.__table,
                values=row.execute_query,
            ),
            params=row.execute_params,
        )
        await self.__db.commit()

    async def read_all(self) -> list[Row]:
        cur: AsyncCursor[Row] = await self.__db.execute(
            query=READ_ALL.format(
                table=self.__table,
            ),
        )
        return await cur.fetchall()

    async def delete_all(self) -> None:
        """Удалить все записи."""
        await self.__db.execute(
            query=DELETE_ALL.format(
                table=self.__table,
            ),
        )
