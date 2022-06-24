"""Create systemd service file."""

import getpass
import os

path = os.getcwd()

POETRY_BIN = "/root/.local/bin/poetry"


def run(service_name: str, description: str) -> None:
    """Создать сервис."""
    service = f"""
[Unit]
Description={description}
[Service]
Restart=on-failure
RestartSec=10s
Type=simple
User={getpass.getuser()}
Group={getpass.getuser()}
EnvironmentFile=/etc/environment
WorkingDirectory={path}
ExecStart={POETRY_BIN} run python start.py
[Install]
WantedBy=multi-user.target"""
    service_file = open(f"setup/{service_name}", "w")
    service_file.write(service)
    service_file.close()
    os.system(f"sudo mv setup/{service_name} /etc/systemd/system")
    os.system("sudo systemctl daemon-reload")
