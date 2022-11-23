"""Синхронизация кода."""

import logging
import os
from typing import Final

from .internal.base_task import BaseTask

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

CMD: Final[str] = (
    "rsync -vhra . {remote_path} --include='**.gitignore' --exclude='/.git' "
    + "--filter=':- .gitignore' --delete-after {dry_run}"
)


class CodeSync(BaseTask):
    """Синхронизация кода."""

    def __init__(
        self,
        desc: str,
        need_confirm: bool = True,
        remote_path: str = "user@target:/destination/project/",
        dry_run: bool = False,
    ) -> None:
        """Базовый класс для задачи.

        Parameters
        ----------
        desc: str
            Описание задачи
        need_confirm: bool
            Требуется подтверждение запуска
        remote_path: str
            ssh-путь на удаленной машине
        dry_run: bool
            проверка выполнения без синхронизации
        """
        super().__init__(desc, need_confirm)
        self.__remote_path = remote_path
        self.__dry_run = dry_run

    def _execute(self) -> None:
        command = CMD.format(
            remote_path=self.__remote_path,
            dry_run="--dry-run" if self.__dry_run else "",
        )
        log.info("Выполнение команды:\n{0}".format(command))
        os.system(command)  # noqa: S605
