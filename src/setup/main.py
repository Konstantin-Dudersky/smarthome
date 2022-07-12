#!/usr/bin/env python3
"""Скрипты установки.

cmd_in_dir = src.cmd_in_dir(work_dir='../server', command='poetry update')
server_git_sync = src.git_sync()
client_ng_build = src.ng_build(work_dir_relative="../client", project="client")
client_ng_dist = src.ng_dist(
    source_dir_rel="../client",
    target_dir_rel="../server/static",
    project="client",
)
server_poetry_install = src.poetry()
server_port_redirect = src.port_redirect(from_port=80, to_port=8000)
"""

import os
import sys

import src


SYSTEMD_SERVICE = 'smarthome'

client_ng_build = src.ng_build(work_dir_relative="../client", project="client")
client_ng_dist = src.ng_dist(
    source_dir_rel="../client",
    target_dir_rel="../server/static",
    project="client",
)
client_tauri_build = src.tauri_build(
    work_dir_relative="../client",
    project="client",
)
server_git_sync = src.git_sync()
server_lint = src.cmd_in_dir(
    work_dir='../server', 
    command='poetry run poe lint',
)
server_poetry_install = src.poetry()
server_poetry_update = src.cmd_in_dir(
    work_dir="../server",
    command="poetry update",
)
server_port_redirect = src.port_redirect(from_port=80, to_port=8000)
server_python = src.python("3.10.5")
server_systemd = src.systemd(
    service_name=SYSTEMD_SERVICE,
    description="Smarthome",
    work_dir_relative="../server",
)


def build() -> None:
    """Сброка проекта."""
    server_lint()
    client_ng_build()


def update() -> None:
    """Обновление проекта."""
    os.system(f"sudo systemctl stop {SYSTEMD_SERVICE}")
    server_poetry_update()
    server_git_sync()
    client_ng_dist()
    os.system(f"sudo systemctl start {SYSTEMD_SERVICE}")


def install() -> None:
    """Первоначальная установка проекта."""
    server_python()
    server_poetry_install()
    server_port_redirect()
    server_systemd()


if __name__ == "__main__":
    match sys.argv[1]:
        case "build":
            build()
        case "install":
            install()
        case "update":
            update()
        case _:
            print(f"Неизвестный параметр: {sys.argv[1]}")
