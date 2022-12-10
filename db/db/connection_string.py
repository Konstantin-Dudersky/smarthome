"""Строка подключения к БД."""

import ipaddress
from dataclasses import dataclass
from typing import Final

from pydantic import SecretStr

CONNECTION_STRING_TEMPL: Final[
    str
] = "{driver}://{user}:{password}@{host}:{port}/{database}"

DEFAULT_IP: Final[ipaddress.IPv4Address] = ipaddress.IPv4Address("127.0.0.1")


@dataclass
class ConnectionString(object):
    """Строка подключения к БД."""

    driver: str = "__driver__"
    user: str = "__user__"
    password: SecretStr = SecretStr("__password__")
    host: ipaddress.IPv4Address = DEFAULT_IP
    port: int = 0
    database: str = "__database__"

    @property
    def url(self) -> str:
        """Строка подключения."""
        return CONNECTION_STRING_TEMPL.format(
            driver=self.driver,
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password.get_secret_value(),
            database=self.database,
        )
