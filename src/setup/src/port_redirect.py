"""Перенаправление портов.

Примеры:

При подключении извне:
sudo iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8000

При подключении локально (localhost):
sudo iptables -t nat -A OUTPUT -o lo -p tcp --dport 80 -j REDIRECT
--to-port 8000

"""

import logging
import os
from typing import Callable

from ._shared import get_logger

log = get_logger(__name__, logging.DEBUG)


def main(from_port: int = 80, to_port: int = 8000) -> Callable[[], None]:
    """Перенаправление портов."""

    def _main() -> None:
        log.info("-> Перенаправление порта %s на порт %s", from_port, to_port)
        os.system("sudo apt install iptables iptables-persistent")
        cmd: str = (
            "sudo iptables -t nat -A PREROUTING -p tcp "
            f"--dport {from_port} -j REDIRECT --to-port {to_port}"
        )
        log.debug("-> Перенаправление внешних подключений:\n%s", cmd)
        os.system(cmd)
        cmd: str = (
            "sudo iptables -t nat -A OUTPUT -o lo -p tcp "
            f"--dport {from_port} -j REDIRECT --to-port {to_port}"
        )
        log.debug("-> Перенаправление внутренних подключений:\n%s", cmd)
        os.system(cmd)
        os.system('sudo sh -c "iptables-save > /etc/iptables/rules.v4"')
        # log.warning(
        #     "-> Если при перезагрузке редирект не сохраняется, "
        #     "то дописать в файл "
        #     ":\n/etc/rc.local\nстроку:\niptables-restore "
        #     "< /etc/iptables.rules",
        # )

    return _main
