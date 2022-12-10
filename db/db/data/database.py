"""Подключение к БД."""

import logging
from typing import Type

from ..connection_string import ConnectionString
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

        self.__conn_str = conn_str
        self.__conn_str.driver = "postgresql"
        self.__conn_str.database = "db_data"
        log.info("DB connection string: {0}".format(conn_str.url))

    def create_session(self, model: Type[TDataModel]) -> Session[TDataModel]:
        """Создает сессию подключения к БД.

        Parameters
        ----------
        model: BaseModel
            модель pydantic для получаемых данных

        Returns
        -------
        Контекстный менеджер для подключения к БД.
        """
        return Session(self.__conn_str.url, model)
