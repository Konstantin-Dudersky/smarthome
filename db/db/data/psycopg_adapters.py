"""Пользовательские адаптеры для psycopg."""

import arrow
import psycopg
from psycopg.adapt import Dumper, Loader


class ArrowLoader(Loader):
    """Загрузка меток времени из БД."""

    def load(self, data: bytes) -> arrow.Arrow:  # noqa: WPS110
        """Загрузка."""
        return arrow.get(data.decode())


class ArrowDamper(Dumper):
    """Сохранение меток времени в БД."""

    def dump(self, obj: arrow.Arrow) -> bytes:  # noqa: WPS110
        """Сохранение."""
        return obj.isoformat().encode()


def register_adapters() -> None:
    """Регистрация пользовательских адаптеров."""
    psycopg.adapters.register_loader("timestamptz", ArrowLoader)
    psycopg.adapters.register_dumper(arrow.Arrow, ArrowDamper)
