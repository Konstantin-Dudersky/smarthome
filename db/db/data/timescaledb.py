"""Работа с таблицами timescaledb."""


import asyncio
import ipaddress
import logging
from types import TracebackType
from typing import Final, Type

import psycopg
from typing_extensions import Self

from . import models2

log: logging.Logger = logging.getLogger(__name__)
log.setLevel(logging.INFO)


DEFAULT_IP: ipaddress.IPv4Address = ipaddress.IPv4Address("0.0.0.0")


def connection_string(
    password: str,
    user: str = "postgres",
    host: ipaddress.IPv4Address = DEFAULT_IP,
    port: int = 5432,
) -> str:
    """Собирает строку подключения.

    :param user: пользователь
    :param password: пароль
    :param host: ip адрес
    :param port: порт
    :return: строка подключения к БД
    """
    return "postgresql://{user}:{password}@{host}:{port}/db_data".format(
        user=user,
        password=password,
        host=host,
        port=port,
    )


class GetDbRow(object):
    """Контекстный менеджер db_data. Тип models.Row."""

    __url: str

    def __init__(self: Self, url: str) -> None:
        """Контекстный менеджер db_data. Тип models.Row.

        :param url: строка подключения к db_data
        """
        self._conn: psycopg.AsyncConnection[models2.Row] | None = None
        self.__url = url

    async def __aenter__(self: Self) -> psycopg.AsyncConnection[models2.Row]:
        """Enter the runtime context related to this object.

        :return: объект подключения к БД
        """
        factory: str = (
            models2.Row.row_factory  # pyright: ignore[reportGeneralTypeIssues]
        )
        self._conn = await psycopg.AsyncConnection.connect(
            conninfo=self.__url,
            row_factory=factory,
            autocommit=True,
        )
        return self._conn  # pyright: ignore[reportUnknownVariableType]

    async def __aexit__(
        self: Self,
        exc_type: Type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit the runtime context related to this object.

        :param exc_type: exc_type
        :param exc_value: exc_value
        :param traceback: traceback
        """
        if self._conn is None:
            return
        await self._conn.close()


CREATE_TYPE: str = """
DO $$ begin
    CREATE TYPE {name} AS ENUM {values};
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;
"""


async def create_agg_type(url: str) -> None:
    """Создать тип перечисления аггрегаций.

    :param url: строка подключения
    """
    stmt: str = CREATE_TYPE.format(
        name="agg_type",
        values=str(tuple(agg.value for agg in models2.AggEnum)),
    )
    log.info("create ENUM agg_type: %s", stmt)
    async with GetDbRow(url) as db:
        await db.execute(stmt)


# async def create_status_type(url: str) -> None:
#     """Создать тип перечисления статуса значения.

#     :param url: строка подключения
#     """
#     stmt: str = CREATE_TYPE.format(
#         name="status_type",
#         values=str(tuple(status.value for status in models.StatusEnum)),
#     )
#     log.info("create ENUM status_type: %s", stmt)
#     async with GetDbRow(url) as db:
#         await db.execute(stmt)


CREATE_TABLE_TEMPL: Final[
    str
] = """
CREATE TABLE {tablename} (
    ts          TIMESTAMPTZ       NOT NULL,
    entity      NUMERIC           NOT NULL,
    attr        VARCHAR(128)      NOT NULL,
    value       DOUBLE PRECISION  NULL,
    status      STATUS_TYPE       NOT NULL,
    agg         AGG_TYPE          NOT NULL,
    aggts       TIMESTAMPTZ       NULL,
    aggnext     AGG_TYPE[]        NULL,
    UNIQUE (ts, entity, attr, agg)
);"""

CREATE_HYPER_TEMPL: Final[
    str
] = """
SELECT create_hypertable(
    '{tablename}', 'ts',
    chunk_time_interval => INTERVAL '{chunk_interval_hours} hours'
);
"""

SET_COMPRESS_TEMPL: Final[
    str
] = """
ALTER TABLE {tablename} SET (
    timescaledb.compress,
    timescaledb.compress_segmentby='entity, attr, agg'
);
"""

COMPRESS_POLICY_TEMPL: Final[
    str
] = """
SELECT add_compression_policy(
    '{tablename}',
    INTERVAL '{compress_policy_hours} hours');
"""


class Table(object):
    """Работа с таблицами timescaledb."""

    __tablename: str
    __url: str

    def __init__(
        self,
        tablename: str,
    ) -> None:
        """Работа с таблицами timescaledb.

        Parameters
        ----------
        tablename: str
            Название таблицы
        """
        self.__tablename = tablename

    def create_table(
        self,
        chunk_interval_hours: int,
        compress_policy_hours: int,
    ) -> None:
        """Создать таблицу.

        Parameters
        ----------
        chunk_interval_hours: int
            Период времени в одном фрагменте, [час]
        compress_policy_hours: int
            Сжимать фрагменты ранее, [час]
        """
        create_table_sql: str = CREATE_TABLE_TEMPL.format(
            tablename=self.__tablename,
        )
        create_hyper_sql: str = CREATE_HYPER_TEMPL.format(
            tablename=self.__tablename,
            chunk_interval_hours=chunk_interval_hours,
        )
        set_compress_sql: str = SET_COMPRESS_TEMPL.format(
            tablename=self.__tablename,
        )
        compress_policy_sql: str = COMPRESS_POLICY_TEMPL.format(
            tablename=self.__tablename,
            compress_policy_hours=compress_policy_hours,
        )

    async def create(self: Self) -> None:
        """Создать таблицу."""
        log.info("Начинаем создавать таблицу %s", self.__tablename)
        async with GetDbRow(self.__url) as db:
            try:
                for stmt in [
                    self.create_table_sql(),
                    self.create_hypertable_sql(),
                    self.set_compress(),
                    self.compression_policy(),
                ]:
                    log.debug("execute stmt:%s", stmt)
                    await db.execute(stmt)
                log.info("Таблица %s создана.", self.__tablename)
            except psycopg.errors.DuplicateTable:
                log.error("Таблица %s уже есть в БД", self.__tablename)


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
