"""Вызвать функцию с параметрами, в указанной папке."""

import inspect
import logging
import os
from typing import Callable

from ..internal.shared import dir_rel_to_abs

log: logging.Logger = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def call_func(
    work_dir_rel: str,
    func: Callable[[], None],
) -> Callable[[], None]:
    def _task() -> None:
        work_dir_abs: str = dir_rel_to_abs(work_dir_rel)
        log.info(
            "Выполняем функцию: {0},\nв папке: {1}".format(
                inspect.getsource(func),
                work_dir_abs,
            )
        )
        os.chdir(work_dir_abs)
        func()

    return _task
