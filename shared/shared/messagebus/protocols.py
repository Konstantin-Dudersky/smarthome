from abc import abstractmethod
from typing import Protocol


class MessagebusProtocolAppend(Protocol):
    @abstractmethod
    def append(self, message: str) -> None:
        """Добавить сообщение."""


class MessagebusProtocolPop(Protocol):
    @abstractmethod
    def pop(self) -> str:
        """Достать сообщение из стека."""
