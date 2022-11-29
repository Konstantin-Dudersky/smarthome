"""Параллельный запуск асинхронных задач."""

from .tasks_protocol import TasksProtocol
from .tasks_runner import TasksRunner

__all__ = [
    "TasksProtocol",
    "TasksRunner",
]
