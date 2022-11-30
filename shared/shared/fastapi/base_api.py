"""FastAPI."""

import abc
from typing import Coroutine, Iterable

import uvicorn
from fastapi import FastAPI

from ..async_tasks import TasksProtocol


class BaseApi(abc.ABC, TasksProtocol):
    """FastAPI."""

    def __init__(self, port: int = 8000) -> None:
        """FastAPI."""
        self.__port = port
        self.__app = FastAPI()

    @property
    def app(self) -> FastAPI:
        """Return FastAPI application."""
        return self.__app

    @property
    def async_tasks(self) -> Iterable[Coroutine[None, None, None]]:
        """Перечень задач для запуска."""
        return {self.__task()}

    async def __task(self):
        config = uvicorn.Config(
            self.__app,
            host="0.0.0.0",
            port=self.__port,
            log_level="info",
        )
        server = uvicorn.Server(
            config,
        )
        await server.serve()
