"""Прослойка для приложения FastAPI."""

from fastapi import Depends, FastAPI, HTTPException, Path, Query, status

from .base_api import BaseApi
from .base_dependencies import BaseDependencies

__all__ = [
    "BaseApi",
    "BaseDependencies",
    "Depends",
    "FastAPI",
    "HTTPException",
    "Path",
    "Query",
    "status",
]
