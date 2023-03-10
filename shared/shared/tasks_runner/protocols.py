from abc import abstractmethod
from typing import Coroutine, Protocol

TCoro = Coroutine[None, None, None]


class ITaskRunnerAdd(Protocol):
    @abstractmethod
    def add_task(self, name: str, coro: TCoro) -> None:
        """Добавить задачу для циклического."""
