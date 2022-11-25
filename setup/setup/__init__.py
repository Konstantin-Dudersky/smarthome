"""Скрипты установки."""

from .tasks.code_sync import CodeSync
from .tasks.docker_move_images import DockerMoveImages
from .tasks.simple_command import SimpleCommand, SimpleCommandMultifolder
from .internal.base_task import BaseTask
from .internal.compose_task import ComposeTask

from .tasks import call_func
from .tasks import docker_tasks
from .tasks import systemd
from .tasks import user_intercation
from .tasks.create_folder_abs import main as create_folder_abs
from .tasks.create_folder_rel import main as create_folder_rel
from .tasks.main import Runner
from .tasks.ng_build import main as ng_build
from .tasks.ng_dist import main as ng_dist
from .tasks.pgadmin import main as pgadmin
from .tasks.poetry import poetry_self_install, poetry_self_update
from .tasks.port_redirect import main as port_redirect
from .tasks.postgresql_add_db import main as postgresql_add_db
from .tasks.postgresql_install import main as postgresql_install
from .tasks.python import main as python
from .tasks.samba import main as samba
from .tasks.tauri_build import main as tauri_build
from .tasks.timescaledb_install import main as timescaledb_install
from .tasks.timescaledb_update_db import main as timescaledb_update_db

__all__ = [
    "SimpleCommand",
    "SimpleCommandMultifolder",
    "BaseTask",
    "ComposeTask",
    "CodeSync",
    "DockerMoveImages",
    "Runner",
    "call_func",
    "create_folder_abs",
    "create_folder_rel",
    "docker_tasks",
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
    "systemd",
    "tauri_build",
    "timescaledb_install",
    "timescaledb_update_db",
    "user_intercation",
]
