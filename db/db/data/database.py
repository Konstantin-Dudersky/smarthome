"""Подключение к БД db_data."""


import asyncio
from ipaddress import IPv4Address
import logging
from types import TracebackType
from typing import Final, Type

import psycopg
from typing_extensions import Self

from . import models

log: logging.Logger = logging.getLogger(__name__)
log.setLevel(logging.INFO)


URL: Final[
    str
] = "postgresql+{driver}://{user}:{password}@{host}:{port}/db_data"


class GetDbRow(object):
    """Контекстный менеджер db_data. Тип models.Row."""

    __url: str

    def __init__(self, url: str) -> None:
        """Контекстный менеджер db_data. Тип models.Row.

        Parameters
        ----------
        url: str
            Строка подключения к db_data
        """
        self._conn: psycopg.AsyncConnection[models.Row] | None = None
        self.__url = url

    async def __aenter__(self) -> psycopg.AsyncConnection[models.Row]:
        """Enter the runtime context related to this object.

        Returns
        -------
        Объект подключения к БД
        """
        factory: str = (
            models.Row.row_factory  # pyright: ignore[reportGeneralTypeIssues]
        )
        self._conn = await psycopg.AsyncConnection.connect(
            conninfo=self.__url,
            row_factory=factory,
            autocommit=True,
        )
        return self._conn  # pyright: ignore[reportUnknownVariableType]

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit the runtime context related to this object.

        Parameters
        ----------
        exc_type
            exc_type
        exc_value
            exc_value
        traceback
            traceback
        """
        if self._conn is None:
            return
        await self._conn.close()


class DbData(object):
    """Подключение к БД db_data."""

    __host: IPv4Address
    __port: int
    __user: str
    __password: str

    def __init__(
        self,
        *,
        host: IPv4Address,
        port: int = 5432,
        user: str = "postgres",
        password: str,
    ) -> None:
        """Подключение к БД db_conf.

        Parameters
        ----------
        host: IPv4Address
            ip адрес
        port: int
            порт
        user: str
            пользователь
        password: str
            пароль
        """
        self.__host = host
        self.__port = port
        self.__user = user
        self.__password = password

    @property
    def connection_string(self) -> str:
        """Возвращает строку подключения.

        Returns
        -------
        Строка подключения
        """
        return URL.format(
            driver="psycopg3",
            host=self.__host,
            port=self.__port,
            user=self.__user,
            password=self.__password,
        )

    def cm(self):
        return GetDbRow(self.connection_string)


CHUNK_INTERVAL: int = 60
COMP_POLICY_HOURS: int = 1000000


def create_db_data_scheme(url: str) -> None:
    """Создание таблиц в БД.

    :param url: строка подключения
    """

    async def _create_db_data_scheme() -> None:
        await create_agg_type(url)
        await create_status_type(url)
        await Table(
            url=url,
            tablename="raw",
            chunk_interval=CHUNK_INTERVAL,
            comp_policy_hours=COMP_POLICY_HOURS,
        ).create()
        await Table(
            url=url,
            tablename="agg_3min",
            chunk_interval=CHUNK_INTERVAL,
            comp_policy_hours=COMP_POLICY_HOURS,
        ).create()
        await Table(
            url=url,
            tablename="agg_30min",
            chunk_interval=CHUNK_INTERVAL,
            comp_policy_hours=COMP_POLICY_HOURS,
        ).create()
        await Table(
            url=url,
            tablename="agg_1day",
            chunk_interval=CHUNK_INTERVAL,
            comp_policy_hours=COMP_POLICY_HOURS,
        ).create()
        await Table(
            url=url,
            tablename="agg_1month",
            chunk_interval=CHUNK_INTERVAL,
            comp_policy_hours=COMP_POLICY_HOURS,
        ).create()

    asyncio.run(_create_db_data_scheme())
