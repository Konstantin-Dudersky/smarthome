"""Пакет для управления настройками приложения."""

from .schema import SettingsSchema
from .settings import SettingsStore

__all__ = [
    "SettingsSchema",
    "SettingsStore",
]
