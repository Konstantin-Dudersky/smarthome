"""CRUD операции над строками."""

# pyright: reportUnknownMemberType=false

from typing import Any, Final, Sequence

from psycopg import AsyncConnection, AsyncCursor

from ..models import Row
from .const import CHUNK_SIZE
from .utils.divide_chunks import divide_chunks

CREATE: Final[
    str
] = """
INSERT INTO {table}
VALUES {values}
ON CONFLICT (ts, entity, attr, agg) DO UPDATE
    SET value = excluded.value,
        status = excluded.status,
        aggts = excluded.aggts;
"""

READ_ALL: Final[str] = "SELECT * FROM {table}"

DELETE_ALL: Final[str] = "DELETE FROM {table}"


class CrudRows(object):
    """CRUD операции над строками."""

    def __init__(self, db: AsyncConnection[Row], table: str) -> None:
        """CRUD операции над строками."""
        self.__db: AsyncConnection[Row]
        self.__table: str

        self.__db = db
        self.__table = table

    async def create_one(self, row: Row) -> None:
        """Создать одну строку."""
        await self.__db.execute(
            query=CREATE.format(
                table=self.__table,
                values=row.format_psycopg.query,
            ).encode(),
            params=row.format_psycopg.params,
        )
        await self.__db.commit()

    async def create_many(self, rows: Sequence[Row]) -> None:
        """Создать несколько строк."""
        chunk_size: int = CHUNK_SIZE // Row.num_of_fields
        for chunk_rows in divide_chunks(rows, chunk_size):
            query_values: list[str] = [
                row.format_psycopg.query for row in chunk_rows
            ]
            query_values_joined = ",".join(query_values)
            params_in_single_list: list[Any] = [
                par for row in chunk_rows for par in row.format_psycopg.params
            ]
            await self.__db.execute(
                query=CREATE.format(
                    table=self.__table,
                    values=query_values_joined,
                ).encode(),
                params=params_in_single_list,
            )
            await self.__db.commit()

    async def read_all(self) -> list[Row]:
        """Прочитать все записи в БД."""
        cur: AsyncCursor[Row] = await self.__db.execute(
            query=READ_ALL.format(
                table=self.__table,
            ).encode(),
        )
        return await cur.fetchall()

    async def delete_all(self) -> None:
        """Удалить все записи."""
        await self.__db.execute(
            query=DELETE_ALL.format(
                table=self.__table,
            ).encode(),
        )
