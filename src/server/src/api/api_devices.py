"""API для доступа к устройствам."""

from fastapi import APIRouter, Query

from src.deconz.sensors import Humidity, OpenClose, ZHAPressure, ZHATemperature
from src.devices.main import (
    bulb,
    sensor_humidity,
    sensor_open_close,
    sensor_temperature,
    sensor_pressure,
)
from src.yeelight import BulbSchema

router = APIRouter(
    prefix="/api/devices",
    tags=["scanner"],
)


@router.get("/")
async def get() -> None:
    """Получить информацию от сканера."""
    return


# yeelight ---------------------------------------------------------------------


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
    bulb.data.power.write(power)


@router.get("/yeelight/{device_id}/set-bright")
async def set_bright(
    device_id: str,
    bright: int,
) -> None:
    """Изменить яркость лампы.

    :param device_id: id устройства
    :param bright: яркость лампы в процентах
    """
    # await bulb.set_bright(bright)
    bulb.data.bright.write(bright)


@router.get("/yeelight/{device_id}/set-ct")
async def set_ct(
    device_id: str,
    ct_value: int = Query(..., alias="ctValue"),
) -> None:
    """Изменить цветовую температуру.

    :param device_id: id устройства
    :param ct_value: цветовая температура (1700-6500K)
    """
    bulb.data.ct.write(ct_value)


@router.get("/yeelight/{device_id}/set-rgb")
async def set_rgb(
    device_id: str,
    rgb_value: int = Query(..., alias="rgbValue"),
) -> None:
    """Изменить цветовую температуру.

    :param device_id: id устройства
    :param rgb_value: цвет RGB (0-16777215)
    """
    bulb.data.rgb.write(rgb_value)


# deconz -----------------------------------------------------------------------


@router.get(
    "/deconz/zhaopenclose/{device_id}",
    response_model=OpenClose.Schema,
)
async def deconz_zhaopenclose(
    device_id: str,
) -> OpenClose.Schema:
    """Данные датчика ZHAOpenClose.

    :param device_id: id устройства
    :return: данные датчика
    """
    return sensor_open_close.schema


@router.get(
    "/deconz/zhahumidity/{device_id}",
    response_model=Humidity.Schema,
)
async def deconz_zhahumidity(
    device_id: str,
) -> Humidity.Schema:
    """Данные датчика ZHAHumidity.

    :param device_id: id устройства
    :return: данные датчика
    """
    return sensor_humidity.schema


@router.get(
    "/deconz/zhatemperature/{device_id}",
    response_model=ZHATemperature.Schema,
)
async def deconz_zhatemperature(
    device_id: str,
) -> ZHATemperature.Schema:
    """Данные датчика ZHATemperature.

    :param device_id: id устройства
    :return: данные датчика
    """
    return sensor_temperature.schema


@router.get(
    "/deconz/zhapressure/{device_id}",
    response_model=ZHAPressure.Schema,
)
async def deconz_zhapressure(
    device_id: str,
) -> ZHAPressure.Schema:
    """Данные датчика ZHAPressure.

    :param device_id: id устройства
    :return: данные датчика
    """
    return sensor_pressure.schema
