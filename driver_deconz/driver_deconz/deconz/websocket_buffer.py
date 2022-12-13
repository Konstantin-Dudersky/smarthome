"""Буфер сообщений websocket."""

import logging
from typing import Final, NamedTuple

from .exceptions import BufferEmptyError

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

MAX_BUFFER_SIZE: Final[int] = 10


class WebsocketBufferItem(NamedTuple):
    """Запись в буфере сообщений."""

    uniqueid: str
    state: str


class WebsocketBuffer(object):
    """Буфер сообщений websocket."""

    def __init__(self) -> None:
        """Буфер сообщений websocket."""
        self.__buffer: list[WebsocketBufferItem] = []

    def put(self, message: WebsocketBufferItem) -> None:
        """Добавить сообщение в буфер."""
        log.debug("new message in buffer:\n{0}".format(message))
        buffer_len = len(self.__buffer)
        if buffer_len >= MAX_BUFFER_SIZE:
            log.warning("message buffer full, len: {0}".format(buffer_len))
            self.__buffer.pop(0)
        self.__buffer.append(message)

    def get(self) -> WebsocketBufferItem:
        """Возвращает и удаляет сообщение из буфера."""
        try:
            message = self.__buffer.pop(0)
        except IndexError as exc:
            raise BufferEmptyError from exc
        log.debug("remove message from buffer:\n{0}".format(message))
        return message
