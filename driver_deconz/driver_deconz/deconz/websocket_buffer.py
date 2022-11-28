"""Буфер сообщений websocket."""

import logging
from typing import Any, Final

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

MAX_BUFFER_SIZE: Final[int] = 10

TMessage = dict[str, Any]


class WebsocketBuffer(object):
    """Буфер сообщений websocket."""

    def __init__(self) -> None:
        """Буфер сообщений websocket."""
        self.__buffer: list[TMessage] = []

    def put(self, message: TMessage) -> None:
        """Добавить сообщение в буфер."""
        log.debug("new message in buffer:\n{0}".format(message))
        buffer_len = len(self.__buffer)
        if buffer_len >= MAX_BUFFER_SIZE:
            log.warning("message buffer full, len: {0}".format(buffer_len))
            self.__buffer.pop(0)
        self.__buffer.append(message)

    def get(self) -> TMessage | None:
        """Возвращает и удаляет сообщение из буфера."""
        if not self.__buffer:
            return None
        message = self.__buffer.pop(0)
        log.debug("remove message from buffer:\n{0}".format(message))
        return message
