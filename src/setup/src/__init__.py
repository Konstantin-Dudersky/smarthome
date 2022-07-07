"""Скрипты установки."""

from .cmd_in_dir import main as cmd_in_dir
from .git_sync import main as git_sync
from .ng_build import main as ng_build
from .ng_dist import main as ng_dist
from .poetry import main as poetry
from .port_redirect import main as port_redirect
from .python import main as python
from .systemd import main as systemd
from .tauri_build import main as tauri_build

__all__ = [
    "cmd_in_dir",
    "git_sync",
    "ng_build",
    "ng_dist",
    "poetry",
    "port_redirect",
    "python",
    "systemd",
    "tauri_build",
]
