"""Базовый класс сообщения."""

from typing import Self, Type

from pydantic import BaseModel, validator


class BaseMessage(BaseModel):
    """Базовый класс сообщения."""

    entity_id: str
    class_name: str | None = None

    @validator("class_name", pre=True, always=True)
    def validate_class_name(
        cls: Type[Self],  # type: ignore
        class_name: str | None,
    ) -> str:
        """Установить имя класса."""
        return class_name or cls.__name__
