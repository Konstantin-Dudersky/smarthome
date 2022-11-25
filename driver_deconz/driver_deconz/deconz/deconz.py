"""Получение данных с сервера Deconz."""

# pyright: reportUnknownMemberType=false

import asyncio
import logging
from enum import Enum, auto
from typing import NamedTuple

import pydantic

from websockets import client, exceptions

from src.utils.settings import settings

from .api.api import get_config
from . import schemas


log: logging.Logger = logging.getLogger(__name__)
log.setLevel(logging.INFO)

DECONZ_REST_URL = (
    f"http://{settings.deconz_ip}:{settings.deconz_rest_port}"
    f"/api/{settings.deconz_api_key}"
)


class States(Enum):
    """Состояния подключения websocket."""

    INIT = auto()  # конфигурация не получена
    CONFIG_RCV = auto()  # конфигурация получена
    CONNECTED = auto()  # подключено
    RECONNECT = auto()  # подключение пропало, переподключаемся


class MessageBuffer(NamedTuple):
    """Буфер сообщений websocket."""

    zha_open_close: dict[int, schemas.ZHAOpenCloseWs] = {}
    zha_presence: dict[int, schemas.ZHAPresenceWs] = {}
    zha_light_level: dict[int, schemas.ZHALightLevelWs] = {}
    zha_humidity: dict[int, schemas.ZHAHumidityWs] = {}
    zha_temperature: dict[int, schemas.ZHATemperatureWs] = {}
    zha_pressure: dict[int, schemas.ZHAPressureWs] = {}
    without_state: dict[int, schemas.WsMsg] = {}


class Websocket:
    """Подключение через websocket."""

    def __init__(self: "Websocket") -> None:
        """Подключение через websocket."""
        self.__state = States.INIT
        self.__websocketport: int = 0
        self.__msg: MessageBuffer = MessageBuffer()

    async def task(self: "Websocket") -> None:
        """Основной цикл."""
        while True:
            await self.__task()

    def get_msg_general(
        self: "Websocket",
        resource_id: int,
    ) -> schemas.WsMsg | None:
        """Иногда deconz публикует сообщение без state.

        :param resource_id: id датчика
        :return: Сообщение из буфера или None
        """
        return self.__msg.without_state.pop(resource_id, None)

    def get_msg_open_close(
        self: "Websocket",
        resouce_id: int,
    ) -> schemas.ZHAOpenCloseWs | None:
        """Возвращает сообщение из очереди для датчика ZHAOpenClose.

        :param resouce_id: id датчика
        :return: Сообщение из буфера или None
        """
        return self.__msg.zha_open_close.pop(resouce_id, None)

    def get_msg_light_level(
        self: "Websocket",
        resouce_id: int,
    ) -> schemas.ZHALightLevelWs | None:
        """Возвращает сообщение из очереди для датчика ZHALightLevel.

        :param resouce_id: id датчика
        :return: Сообщение из буфера или None
        """
        return self.__msg.zha_light_level.pop(resouce_id, None)

    def get_msg_presence(
        self: "Websocket",
        resouce_id: int,
    ) -> schemas.ZHAPresenceWs | None:
        """Возвращает сообщение из очереди для датчика ZHAPresence.

        :param resouce_id: id датчика
        :return: Сообщение из буфера или None
        """
        return self.__msg.zha_presence.pop(resouce_id, None)

    def get_msg_humidity(
        self: "Websocket",
        resouce_id: int,
    ) -> schemas.ZHAHumidityWs | None:
        """Возвращает сообщение из очереди для датчика ZHAHumidity.

        :param resouce_id: id датчика
        :return: Сообщение из буфера или None
        """
        return self.__msg.zha_humidity.pop(resouce_id, None)

    def get_msg_pressure(
        self: "Websocket",
        resouce_id: int,
    ) -> schemas.ZHAPressureWs | None:
        """Возвращает сообщение из очереди для датчика ZHAPressure.

        :param resouce_id: id датчика
        :return: Сообщение из буфера или None
        """
        return self.__msg.zha_pressure.pop(resouce_id, None)

    def get_msg_temperature(
        self: "Websocket",
        resouce_id: int,
    ) -> schemas.ZHATemperatureWs | None:
        """Возвращает сообщение из очереди для датчика ZHATemperature.

        :param resouce_id: id датчика
        :return: Сообщение из буфера или None
        """
        return self.__msg.zha_temperature.pop(resouce_id, None)

    async def _get_config(self: "Websocket") -> None:
        """Получить номер порта."""
        config = await get_config()
        if config is None:
            await asyncio.sleep(0)
            return
        self.__websocketport = config.websocketport
        self.__state = States.CONFIG_RCV

    async def __task(self: "Websocket") -> None:
        """Основной цикл."""
        log.debug(self.__state.name)
        match self.__state:
            case States.INIT:
                await self._get_config()
            case States.CONFIG_RCV:
                await self._connect()
            case States.CONNECTED:
                await self._connect()
            case States.RECONNECT:
                await self._connect()
                await asyncio.sleep(1)

    async def _connect(self: "Websocket") -> None:
        """Получение данных по websocket."""
        ws_url = f"ws://{settings.deconz_ip}:{self.__websocketport}"
        async for websocket in client.connect(ws_url):
            try:
                data = await websocket.recv()
                self._parse_msg(str(data))
            except exceptions.ConnectionClosed:
                continue
            except ValueError:
                log.exception("Неизвестный формат сообщения websocket")

    def _parse_msg(self: "Websocket", data: str) -> None:
        # датчик открыт/закрыт
        try:
            msg1 = schemas.ZHAOpenCloseWs.parse_raw(data)
            self.__msg.zha_open_close[msg1.resource_id] = msg1
            return
        except pydantic.ValidationError:
            pass
        # датчик присутствия
        try:
            msg2 = schemas.ZHAPresenceWs.parse_raw(data)
            self.__msg.zha_presence[msg2.resource_id] = msg2
            return
        except pydantic.ValidationError:
            pass
        # датчик освещенности
        try:
            msg3 = schemas.ZHALightLevelWs.parse_raw(data)
            self.__msg.zha_light_level[msg3.resource_id] = msg3
            return
        except pydantic.ValidationError:
            pass
        # датчик влажности
        try:
            msg4 = schemas.ZHAHumidityWs.parse_raw(data)
            self.__msg.zha_humidity[msg4.resource_id] = msg4
            return
        except pydantic.ValidationError:
            pass
        # датчик давления
        try:
            msg5 = schemas.ZHAPressureWs.parse_raw(data)
            self.__msg.zha_pressure[msg5.resource_id] = msg5
            return
        except pydantic.ValidationError:
            pass
        # датчик температуры
        try:
            msg6 = schemas.ZHATemperatureWs.parse_raw(data)
            self.__msg.zha_temperature[msg6.resource_id] = msg6
            return
        except pydantic.ValidationError:
            pass
        # общее сообщение
        try:
            msg100 = schemas.WsMsg.parse_raw(data)
            self.__msg.without_state[msg100.resource_id] = msg100
            return
        except pydantic.ValidationError as exc:
            log.exception("Неизвестный формат сообщения websocket")
            raise ValueError(
                f"Неизвестный формат сообщения websocket:\n{data}",
            ) from exc


if __name__ == "__main__":
    ws = Websocket()
    asyncio.run(ws.task())
