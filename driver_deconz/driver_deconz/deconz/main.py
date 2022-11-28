"""Основной класс для управления данными."""

import asyncio
import logging
from ipaddress import IPv4Address
from typing import Coroutine, Iterable

from .sensors_collection import SensorCollection
from .websocket import Websocket

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class Deconz(object):
    """Основной класс для управления данными."""

    def __init__(
        self,
        host: IPv4Address,
        port_ws: int,
        sensosrs: SensorCollection,
    ) -> None:
        """Основной класс для управления данными."""
        self.__ws = Websocket(host, port_ws)
        self.__sensors = sensosrs

    @property
    def async_tasks(self) -> Iterable[Coroutine[None, None, None]]:
        """Асинхронные задачи."""
        return {
            self.__ws.task(),
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
