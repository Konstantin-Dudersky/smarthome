from collections import deque

from .protocols import MessagebusProtocolAppend, MessagebusProtocolPop


class MessageBus(MessagebusProtocolAppend, MessagebusProtocolPop):
    def __init__(self, maxlen: int = 100) -> None:
        self.__collection: deque[str] = deque(maxlen=maxlen)

    def append(self, message: str):
        """Добавить сообщение."""
        self.__collection.append(message)

    def pop(self) -> str:
        """Достать сообщение из стека."""
        return self.__collection.popleft()
