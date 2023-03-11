from collections import deque

from .protocols import ISimpleDequeAppend, ISimpleDequePop, T


class SimpleDeque(ISimpleDequeAppend[T], ISimpleDequePop[T]):
    def __init__(self, maxlen: int = 100) -> None:
        self.__collection: deque[T] = deque(maxlen=maxlen)

    def append(self, message: T):
        """Добавить сообщение."""
        self.__collection.append(message)

    def pop(self) -> T:
        """Достать сообщение из стека."""
        return self.__collection.popleft()
