"""Получение данных с устройств по протоколу websocket.

Данные собираются в буфере, который читает внешний модуль.
"""

import json
import logging
from ipaddress import IPv4Address
from typing import Any, Coroutine, Final, Iterable

from shared.async_tasks import TasksProtocol
from websockets import client, exceptions

from .websocket_buffer import WebsocketBuffer, WebsocketBufferItem

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

WS_URL: Final[str] = "ws://{host}:{port}"


class Websocket(TasksProtocol):
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

    @property
    def async_tasks(self) -> Iterable[Coroutine[None, None, None]]:
        """Перечень задач для запуска."""
        return {
            self.__task(),
        }

    def get(self) -> WebsocketBufferItem:
        """Возвращает и удаляет сообщение из буфера."""
        return self.__buffer.get()

    async def __task(self) -> None:
        """Основной цикл."""
        while True:  # noqa: WPS457
            await self.__task_loop()

    async def __task_loop(self) -> None:
        async for websocket in client.connect(self.__url):  # noqa: WPS327
            try:
                await self.__iterate_messages(websocket)
            except exceptions.ConnectionClosed:
                continue
            except TimeoutError:
                log.error("Таймаут подключения по websocket")
                continue

    async def __iterate_messages(
        self,
        websocket: client.WebSocketClientProtocol,
    ) -> None:
        async for message in websocket:
            self.__process_message(str(message))

    def __process_message(self, message: str) -> None:
        message_dict: dict[str, Any] = json.loads(message)
        if "state" not in message_dict:
            return
        buffer_item = WebsocketBufferItem(
            uniqueid=message_dict["uniqueid"],
            state=message_dict["state"],
        )
        self.__buffer.put(buffer_item)
