"""Получение данных с сервера Deconz."""

# pyright: reportUnknownMemberType=false

import asyncio
from enum import Enum, auto
from typing import NamedTuple

import pydantic

from websockets import client, exceptions

from src.utils.logger import get_logger, LoggerLevel
from src.utils.settings import settings

from .api import get_config
from . import models

logger = get_logger(__name__)
logger.setLevel(LoggerLevel.INFO)

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

    zha_open_close: dict[int, models.WsMsgOpenClose] = {}
    without_state: dict[int, models.WsMsgWithoutState] = {}


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
    ) -> models.WsMsgWithoutState | None:
        """Иногда deconz публикует сообщение без state.

        :param resource_id: id датчика
        :return: Сообщение из буфера или None
        """
        return self.__msg.without_state.pop(resource_id, None)

    def get_msg_open_close(
        self: "Websocket",
        resouce_id: int,
    ) -> models.WsMsgOpenClose | None:
        """Возвращает сообщение из очереди для датчика ZHAOpenClose.

        :param resouce_id: id датчика
        :return: Сообщение из буфера или None
        """
        return self.__msg.zha_open_close.pop(resouce_id, None)

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
        logger.debug(self.__state.name)
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
                logger.exception("Неизвестный формат сообщения websocket")

    def _parse_msg(self: "Websocket", data: str) -> None:
        # датчик открыт/закрыт
        try:
            msg1 = models.WsMsgOpenClose.parse_raw(data)
            self.__msg.zha_open_close[msg1.resource_id] = msg1
            return
        except pydantic.ValidationError:
            pass
        # датчик присутствия
        # общее сообщение
        try:
            msg2 = models.WsMsgWithoutState.parse_raw(data)
            self.__msg.without_state[msg2.resource_id] = msg2
            return
        except pydantic.ValidationError:
            pass
        raise ValueError(f"Неизвестный формат сообщения websocket:\n{data}")


if __name__ == "__main__":
    ws = Websocket()
    asyncio.run(ws.task())
