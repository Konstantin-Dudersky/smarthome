"""Скрипты установки."""

from .code_sync import CodeSync
from .simple_command import SimpleCommand
from .internal.base_task import BaseTask
from .internal.compose_task import ComposeTask

from . import call_func
from . import docker_tasks
from . import systemd
from . import user_intercation
from .create_folder_abs import main as create_folder_abs
from .create_folder_rel import main as create_folder_rel
from .main import Task, execute
from .ng_build import main as ng_build
from .ng_dist import main as ng_dist
from .pgadmin import main as pgadmin
from .poetry import poetry_self_install, poetry_self_update
from .port_redirect import main as port_redirect
from .postgresql_add_db import main as postgresql_add_db
from .postgresql_install import main as postgresql_install
from .python import main as python
from .samba import main as samba
from .tauri_build import main as tauri_build
from .timescaledb_install import main as timescaledb_install
from .timescaledb_update_db import main as timescaledb_update_db

__all__ = [
    "SimpleCommand",
    "BaseTask",
    "ComposeTask",
    "CodeSync",
    "Task",
    "call_func",
    "create_folder_abs",
    "create_folder_rel",
    "docker_tasks",
    "execute",
    "ng_build",
    "ng_dist",
    "pgadmin",
    "poetry_self_install",
    "poetry_self_update",
    "port_redirect",
    "postgresql_add_db",
    "postgresql_install",
    "python",
    "samba",
    "simple_command",
    "systemd",
    "tauri_build",
    "timescaledb_install",
    "timescaledb_update_db",
]
