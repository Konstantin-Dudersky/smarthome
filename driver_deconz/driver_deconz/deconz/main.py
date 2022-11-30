"""Основной класс для управления данными."""

import asyncio
import logging
from ipaddress import IPv4Address
from typing import Coroutine, Iterable

from pydantic import SecretStr
from shared.async_tasks import TasksProtocol

from .api import Api
from .api_full_state_parse import ParseFullState
from .exceptions import BufferEmptyError
from .sensors import SensorCollection
from .websocket import Websocket

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


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
            self.__check_api()
            self.__check_ws()
            await asyncio.sleep(0.1)

    def __check_ws(self) -> None:
        try:
            ws_msg = self.__ws.get()
        except BufferEmptyError:
            return
        log.debug("new websocket message:\n{0}".format(ws_msg))
        try:
            sensor = self.__sensors.by_id(ws_msg.uniqueid)
        except ValueError:
            return
        sensor.update_state(ws_msg.state)
        log.debug("updated sensor data:\n{0}".format(sensor))

    def __check_api(self) -> None:
        try:
            full_state_str = self.__api.full_state
        except BufferEmptyError:
            return
        data_by_uniqueid = ParseFullState(full_state_str).data_by_uniqueid
        for api_msg in data_by_uniqueid:
            try:
                sensor = self.__sensors.by_id(api_msg.uniqueid)
            except ValueError:
                continue
            sensor.update_data(api_msg.sensor_data)
