"""Базовый класс сообщения."""


from pydantic import BaseModel


class BaseMessage(BaseModel):
    """Базовый класс сообщения."""

    entity: str
    message_type: str
