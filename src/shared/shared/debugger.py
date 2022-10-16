"""Подключение дебаггера."""

# pylint: disable=import-outside-toplevel

import logging

log: logging.Logger = logging.getLogger(__name__)
log.setLevel(logging.INFO)


def debugger_init(init: bool) -> None:
    """Запуск дебаггера.

    :param init: True = инициализировать
    """
    if not init:
        return

    import debugpy  # noqa: WPS433

    debugpy.listen(("0.0.0.0", 5678))
    log.warning("Запущен режим debug, ждем подключение отладчика")
    debugpy.wait_for_client()
