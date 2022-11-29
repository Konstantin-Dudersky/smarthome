"""Задача для хостинга api."""

from typing import Coroutine, Iterable

import uvicorn
from shared.async_tasks import TasksProtocol

from .main import app


class ApiTask(TasksProtocol):
    """Асинхронная задача для запуска."""

    def __init__(self, port: int = 8000) -> None:
        """Асинхронная задача для запуска."""
        self.__port = port

    @property
    def async_tasks(self) -> Iterable[Coroutine[None, None, None]]:
        """Перечень задач для запуска."""
        return {self.__task()}

    async def __task(self):
        config = uvicorn.Config(
            app,
            host="0.0.0.0",
            port=self.__port,
            log_level="info",
        )
        server = uvicorn.Server(
            config,
        )  # pyright: reportUnknownMemberType=false
        await server.serve()
