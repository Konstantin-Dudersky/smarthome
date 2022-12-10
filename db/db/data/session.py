"""Сессия подключения к БД в виде контекстного менеджера."""

# pyright: reportUnknownMemberType=false

from types import TracebackType
from typing import Generic, Type

import psycopg
from psycopg.rows import class_row

from .typings import TDataModel


class Session(Generic[TDataModel]):
    """Асинхронный контекстный менеджер для подключения к БД."""

    __url: str

    def __init__(self, url: str, model: Type[TDataModel]) -> None:
        """Контекстный менеджер для подключения к БД.

        Parameters
        ----------
        url: str
            строка подключения к db_data
        model: BaseModel
            модель pydantic для получаемых данных
        """
        self.__conn: psycopg.AsyncConnection[TDataModel] | None = None
        self.__url = url
        self.__model: Type[TDataModel] = model

    async def __aenter__(self) -> psycopg.AsyncConnection[TDataModel]:
        """Enter the runtime context related to this object."""
        self.__conn = await psycopg.AsyncConnection.connect(
            conninfo=self.__url,
            row_factory=class_row(self.__model),
            autocommit=True,
        )
        return self.__conn

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit the runtime context related to this object."""
        if self.__conn is None:
            return
        await self.__conn.close()
