"""Классы должны поддерживать общий протокол."""

import abc
from typing import Coroutine, Iterable, Protocol


class TasksProtocol(Protocol):
    """Протокол для запуска асинхронных задач."""

    @property
    @abc.abstractmethod
    def async_tasks(self) -> Iterable[Coroutine[None, None, None]]:
        """Перечень задач для запуска."""
