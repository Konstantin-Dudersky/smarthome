"""Получение данных с сервера Deconz."""

# pyright: reportUnknownMemberType=false

import asyncio
from enum import Enum, auto

from websockets import client, exceptions

from src.utils.logger import get_logger, LoggerLevel
from src.utils.settings import settings

from .api import get_config

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


class Websocket:
    """Подключение через websocket."""

    def __init__(self: "Websocket") -> None:
        """Подключение через websocket."""
        self.__state = States.INIT
        self.__websocketport: int = 0

    async def run(self: "Websocket") -> None:
        """Основной цикл."""
        while True:
            logger.info(self.__state.name)
            match self.__state:
                case States.INIT:
                    await self.get_config()
                case States.CONFIG_RCV:
                    await self.connect()
                case States.CONNECTED:
                    await self.connect()
                case States.RECONNECT:
                    await self.connect()
                    await asyncio.sleep(1)

    async def get_config(self: "Websocket") -> None:
        """Получить номер порта."""
        config = await get_config()
        self.__websocketport = config.websocketport
        self.__state = States.CONFIG_RCV

    async def connect(self: "Websocket") -> None:
        """Получение данных по websocket."""
        ws_url = f"ws://{settings.deconz_ip}:{self.__websocketport}"
        async for websocket in client.connect(ws_url):
            try:
                data = await websocket.recv()
                logger.info("\n %s", data)
            except exceptions.ConnectionClosed:
                continue
            except Exception as exc:
                logger.exception(exc)


if __name__ == "__main__":
    ws = Websocket()
    asyncio.run(ws.run())
