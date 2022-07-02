"""Перенаправление портов."""

import os


def run(from_port: int = 80, to_port: int = 8000) -> None:
    """Перенаправление портов."""
    os.system(
        (
            f"sudo iptables -t nat -A PREROUTING -p tcp --dport {from_port} "
            f" -j REDIRECT --to-port {to_port}"
        ),
    )
    os.system('sudo sh -c "iptables-save > /etc/iptables.rules"')
    os.system("sudo apt-get install iptables-persistent")
