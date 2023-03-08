"""Чтение данных по REST API.

Периодически читает данные и сохраняет в свойстве full_state.
"""

import asyncio
import logging
from ipaddress import IPv4Address
from typing import Coroutine, Final, Iterable

import httpx
from pydantic import SecretStr
from shared.async_tasks import TasksProtocol

from . import exceptions

log: logging.Logger = logging.getLogger(__name__)


BASE_URL: Final[str] = "http://{host}:{port_api}/api/{api_key}"

EXC_REQUEST_ERROR: Final[
    str
] = "Ошибка выполнения запроса\nзапрос: {request}\nсообщение: {message}"


def _construct_full_enpoint(base_url: str, endpoint: str) -> str:
    return "{base_url}{endpoint}".format(
        base_url=base_url,
        endpoint=endpoint,
    )


def _check_status_code(
    code_response: int,
    code_compare: int = httpx.codes.OK,
) -> bool:
    if code_response != code_compare:
        log.error("Incorrect response code: {0}".format(code_response))
        return False
    return True


class Api(TasksProtocol):
    """Чтение данных по REST API."""

    def __init__(
        self,
        host: IPv4Address,
        port_api: int,
        api_key: SecretStr,
        seconds_between_polls: float = 2.0,
        logging_level: int = logging.INFO,
    ) -> None:
        """Чтение данных по REST API."""
        log.setLevel(logging_level)
        self.__base_url = BASE_URL.format(
            host=host,
            port_api=port_api,
            api_key=api_key.get_secret_value(),
        )
        self.__seconds_between_polls = seconds_between_polls
        self.__full_state: str | None = None

    @property
    def async_tasks(self) -> Iterable[Coroutine[None, None, None]]:
        """Перечень задач для запуска."""
        return {self.__task()}

    @property
    def full_state(self) -> str:
        """Возвращает данные. Если данных нет, то BufferEmptyError."""
        if self.__full_state is None:
            raise exceptions.BufferEmptyError
        full_state = self.__full_state
        self.__full_state = None
        return full_state

    async def __task(self) -> None:
        while True:  # noqa: WPS457
            await self.__update_full_state()
            await asyncio.sleep(self.__seconds_between_polls)

    async def __update_full_state(self) -> None:
        log.debug("Start update values from API.")
        try:
            response = await self.__http_query("")
        except exceptions.DataNotReceivedError:
            return
        if not _check_status_code(response.status_code):
            return
        self.__full_state = response.text
        log.debug("Finish update values from API.")

    async def __http_query(self, endpoint: str) -> httpx.Response:
        """Базовый запрос."""
        url = _construct_full_enpoint(self.__base_url, endpoint)
        async with httpx.AsyncClient() as http:
            try:
                return await http.get(url)
            except httpx.RequestError as exc:
                self.__handle_http_query_exc(exc)
                raise exceptions.DataNotReceivedError

    def __handle_http_query_exc(self, exc: httpx.RequestError) -> None:
        log.error(
            EXC_REQUEST_ERROR.format(
                request=exc.request,
                message=str(exc),
            ),
        )
