"""API для доступа к устройствам."""

from fastapi import APIRouter

from src.devices.main import bulb
from src.yeelight import BulbSchema

router = APIRouter(
    prefix="/api/devices",
    tags=["scanner"],
)


@router.get("/")
async def get() -> None:
    """Получить информацию от сканера."""
    return


@router.get("/yeelight/{device_id}", response_model=BulbSchema)
async def get_yeelight(
    device_id: str,
) -> BulbSchema:
    """Возвращает инфо о лампе Yeelight.

    :param device_id: id лампы
    :return: инфо
    """
    return await bulb.get_all_data()


@router.get("/yeelight/{device_id}/set-power")
async def set_power(
    device_id: str,
    power: bool,
) -> None:
    """Включить/выключить.

    :param device_id: id устройства
    :param power: включить или отключить
    """
    await bulb.set_power(power)
