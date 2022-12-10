"""Подключение к БД."""

import logging
from typing import Type

from ..connection_string import ConnectionString
from .psycopg_adapters import register_adapters
from .session import Session
from .typings import TDataModel

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Database(object):
    """Подключение к БД."""

    def __init__(
        self,
        conn_str: ConnectionString,
    ) -> None:
        """Подключение к БД."""
        self.__conn_str: ConnectionString

        register_adapters()
        self.__conn_str = conn_str
        self.__conn_str.driver = "postgresql"
        log.info("DB connection string: {0}".format(conn_str.url))

    def create_session(self, model: Type[TDataModel]) -> Session[TDataModel]:
        """Создает сессию подключения к БД.

        Parameters
        ----------
        model: BaseModel
            модель pydantic для возвращаемых данных

        Returns
        -------
        Контекстный менеджер для подключения к БД.
        """
        return Session(self.__conn_str.url, model)
