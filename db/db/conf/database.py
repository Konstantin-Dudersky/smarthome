"""Подключение к БД db_conf."""

import logging
from ipaddress import IPv4Address
from typing import Final

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    create_async_engine,  # pyright: ignore[reportUnknownVariableType]
)
from sqlalchemy.orm import sessionmaker

log: logging.Logger = logging.getLogger(__name__)
log.setLevel(logging.INFO)


URL: Final[
    str
] = "postgresql+psycopg3://{user}:{password}@{host}:{port}/db_conf"


class DbConf(object):
    """Подключение к БД db_conf."""

    __conn_str: str

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
        self.__conn_str = URL.format(
            user=user,
            password=password,
            host=host,
            port=port,
        )

    @property
    def engine(self) -> AsyncEngine:
        """Create engine for conenction.

        Returns
        -------
        engine
        """
        return create_async_engine(
            url=self.__conn_str,
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
        engine: AsyncEngine = self.engine
        session_maker: sessionmaker[AsyncSession] = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=engine,
            class_=Type[AsyncSession],
        )
        session: AsyncSession = (
            session_maker()
        )  # pyright: ignore[reportGeneralTypeIssues]
        return session
