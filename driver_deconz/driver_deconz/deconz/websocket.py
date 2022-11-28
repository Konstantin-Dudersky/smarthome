"""Получение данных с устройств по протоколу websocket.

Данные собираются в буфере, который читает внешний модуль.
"""

import json
import logging
from ipaddress import IPv4Address
from typing import Final

from websockets import client, exceptions

from .websocket_buffer import TMessage, WebsocketBuffer

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

WS_URL: Final[str] = "ws://{host}:{port}"


class Websocket(object):
    """Получение данных с устройств по протоколу websocket."""

    def __init__(
        self,
        host: IPv4Address,
        port: int,
    ) -> None:
        """Получение данных с устройств по протоколу websocket."""
        self.__url = WS_URL.format(
            host=host,
            port=port,
        )
        self.__buffer = WebsocketBuffer()

    async def task(self) -> None:
        """Основной цикл."""
        while True:  # noqa: WPS457
            await self.__task()

    def get(self) -> TMessage | None:
        """Возвращает и удаляет сообщение из буфера."""
        return self.__buffer.get()

    async def __task(self) -> None:
        async for websocket in client.connect(self.__url):  # noqa: WPS327
            try:
                async for message in websocket:
                    self.__process_message(str(message))
            except exceptions.ConnectionClosed:
                continue

    def __process_message(self, message: str) -> None:
        message_dict: TMessage = json.loads(message)
        if "state" in message_dict:
            self.__buffer.put(message_dict["state"])