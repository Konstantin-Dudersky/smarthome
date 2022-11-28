"""Пакет для управления настройками приложения."""

from .schema import Profiles
from .settings import SettingsStore

__all__ = [
    "Profiles",
    "SettingsStore",
]
