from abc import abstractmethod
from typing import Protocol


class ISimpleDequeAppend(Protocol):
    @abstractmethod
    def append(self, message: str) -> None:
        """Добавить сообщение."""


class ISimpleDequePop(Protocol):
    @abstractmethod
    def pop(self) -> str:
        """Достать сообщение из стека."""
