"""Запуск сервиса."""

import asyncio
from shared.settings import settings_store

setting = settings_store.settings

from .deconz import websocket

if __name__ == "__main__":
    ws = websocket.Websocket("127.0.0.1", 8011)
    asyncio.run(ws.task())
