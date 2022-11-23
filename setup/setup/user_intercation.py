import logging
from typing import Callable

log: logging.Logger = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def confirm(message: str) -> Callable[[], None]:
    def _task() -> None:
        log.warning(message)
        while True:
            log.info("-> Введите y для продолжения: ")
            ans = input()
            if ans == "y":
                break

    return _task
