from abc import abstractmethod
from typing import Generic, Protocol, TypeVar

T = TypeVar("T")
T_cov = TypeVar("T_cov", covariant=True)
T_contra = TypeVar("T_contra", contravariant=True)


class ISimpleDequeAppend(Protocol[T_contra]):
    @abstractmethod
    def append(self, message: T_contra) -> None:
        """Добавить сообщение."""


class ISimpleDequePop(Protocol, Generic[T_cov]):
    @abstractmethod
    def pop(self) -> T_cov:
        """Достать сообщение из стека."""
