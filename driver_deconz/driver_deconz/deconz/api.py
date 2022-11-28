"""Чтение данных REST API."""

import logging

import httpx
from shared.settings import settings_store

from ..schemas import ConfigModel

log: logging.Logger = logging.getLogger(__name__)
log.setLevel(logging.INFO)

settings = settings_store.settings

DECONZ_REST_URL = (
    f"http://{settings.deconz_hub_host}:{settings.deconz_hub_port_api}"
    f"/api/{settings.deconz_hub_api_key}"
)


async def _base_query(endpoint: str) -> httpx.Response | None:
    """Базовый запрос.

    :param endpoint: endpoint
    :return: ответ
    """
    async with httpx.AsyncClient() as http:
        try:
            return await http.get(f"{DECONZ_REST_URL}{endpoint}")
        except httpx.ConnectError as exc:
            log.exception("Ошибка выполнения запроса: %s", exc.request)
            return None


# configuration ----------------------------------------------------------------


async def get_config() -> ConfigModel | None:
    """Return the current gateway configuration.

    :return: конфигурация сервера
    """
    config = await _base_query("/config")
    if config is None:
        return None
    return ConfigModel(**config.json())


# sensors ----------------------------------------------------------------------


async def get_sensor(sensor_id: int) -> httpx.Response | None:
    """Return the sensor with the specified id.

    :param sensor_id: id датчика
    :return: инфо о всех датчиках
    """
    return await _base_query(f"/sensors/{sensor_id}")
