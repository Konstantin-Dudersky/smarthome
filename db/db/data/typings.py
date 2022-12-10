"""Типы данных."""

from typing import TypeVar

from pydantic import BaseModel

TDataModel = TypeVar("TDataModel", bound=BaseModel)
