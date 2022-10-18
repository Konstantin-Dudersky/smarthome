"""Подключение к БД db_conf."""

import logging
from ipaddress import IPv4Address
from typing import Final

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

log: logging.Logger = logging.getLogger(__name__)
log.setLevel(logging.INFO)


URL: Final[
    str
] = "postgresql+{driver}://{user}:{password}@{host}:{port}/db_conf"


class DbConf(object):
    """Подключение к БД db_conf."""

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

    @property
    def connection_string_alembic(self) -> str:
        """Возвращает строку подключения для alembic.

        Returns
        -------
        Строка подключения
        """
        return URL.format(
            driver="asyncpg",
            host=self.__host,
            port=self.__port,
            user=self.__user,
            password=self.__password,
        )

    @property
    def engine(self) -> AsyncEngine:
        """Create engine for conenction.

        Returns
        -------
        engine
        """
        return create_async_engine(
            url=self.connection_string,
            echo=False,
            future=True,
            connect_args={"timeout": 2},
        )

    @property
    def session(self) -> AsyncSession:
        """Create session for db connection.

        Returns
        -------
        Сессия подключения к БД
        """
        session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )
        return session_maker()
