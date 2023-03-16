"""Базовый класс сообщения."""

import datetime as dt
from typing import Self

from pydantic import BaseModel, validator


class BaseMessage(BaseModel):
    """Базовый класс сообщения."""

    entity_id: str
    class_name: str | None = None
    ts: dt.datetime

    @validator("class_name", pre=True, always=True)
    def validate_class_name(
        cls: type[Self],  # type: ignore
        class_name: str | None,
    ) -> str:
        """Установить имя класса."""
        return class_name or cls.__name__
