"""Синхронизация кода."""

import logging
import os
from typing import Final

from ..internal.base_task import BaseTask

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
        """
        super().__init__(desc, need_confirm)
        self.__remote_path = remote_path

    def _execute(self) -> None:
        command = CMD.format(remote_path=self.__remote_path)
        log.debug("Выполнение команды:\n{0}".format(command))
        log.info("Запускаем тестовый прогон:")
        os.system("{0} --dry-run".format(command))  # noqa: S605
        log.info("Синхронизировать файлы? (y/n)")
        ans = input()  # noqa: WPS421
        while True:
            if ans == "y":
                os.system(command)  # noqa: S605
                return
            elif ans == "n":
                return
