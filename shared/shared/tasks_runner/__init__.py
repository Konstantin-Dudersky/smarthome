"""Параллельный запуск асинхронных задач."""

from .tasks_runner import TasksRunner
from .protocols import ITaskRunnerAdd

__all__ = [
    "TasksRunner",
    "ITaskRunnerAdd",
]
