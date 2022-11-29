"""Основной класс для управления данными."""

import asyncio
import logging
from ipaddress import IPv4Address
from typing import Coroutine, Iterable

from pydantic import SecretStr
from shared.async_tasks import TasksProtocol

from .api import Api
from .sensors_collection import SensorCollection
from .websocket import Websocket

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class Deconz(TasksProtocol):
    """Основной класс для управления данными."""

    def __init__(
        self,
        host: IPv4Address,
        port_api: int,
        port_ws: int,
        api_key: SecretStr,
        sensosrs: SensorCollection,
    ) -> None:
        """Основной класс для управления данными."""
        self.__api = Api(
            host=host,
            port_api=port_api,
            api_key=api_key,
            logging_level=logging.DEBUG,
        )
        self.__ws = Websocket(host, port_ws)
        self.__sensors = sensosrs

    @property
    def async_tasks(self) -> Iterable[Coroutine[None, None, None]]:
        """Перечень задач для запуска."""
        return {
            *self.__api.async_tasks,
            *self.__ws.async_tasks,
            self.__task(),
        }

    async def __task(self) -> None:
        """Задача для циклического выполнения."""
        while True:  # noqa: WPS457
            self.__check_ws()
            await asyncio.sleep(0.1)

    def __check_ws(self):
        msg = self.__ws.get()
        if msg is None:
            return
        log.debug("new websocket message:\n{0}".format(msg))
        identificator = int(msg["id"])
        try:
            sensor = self.__sensors.by_id(identificator)
        except ValueError:
            return
        sensor.parse_data(msg["state"])
