"""Коллекция датчиков.

К отдельным датчикам можно обращаться как по id, так и по имени name.
"""

import logging
from typing import Any, Final, Iterable

from shared.patterns import SingletonMeta

from .sensor import Sensor

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

MSG_DUBL_NAME: Final[str] = "Повторяющееся название датчика: {name}"
MSG_DUBL_ID: Final[str] = "Повторяющийся id датчика: {id}"

UNKNOWN_NAME: Final[str] = "Неизвестное название: {name}"
UNKNOWN_ID: Final[str] = "Неизвестный идентификатор: {id}"


class SensorCollection(object, metaclass=SingletonMeta["SensorCollection"]):
    """Коллеция датчиков."""

    def __init__(
        self,
        sensors: Iterable[Sensor[Any]],
    ) -> None:
        """Коллеция датчиков."""
        self.__by_id = self.__create_by_id(sensors)
        self.__by_name = self.__create_by_name(sensors)

    def by_id(self, identificator: int) -> Sensor[Any]:
        """Датчик по идентификатору."""
        if identificator not in self.__by_id:
            msg = UNKNOWN_ID.format(id=identificator)
            log.warning(msg)
            raise ValueError(msg)
        return self.__by_id[identificator]

    def by_name(self, name: str) -> Sensor[Any]:
        """Датчик по названию."""
        if name not in self.__by_name:
            msg = UNKNOWN_NAME.format(name=name)
            log.warning(msg)
            raise ValueError(msg)
        return self.__by_name[name]

    def __create_by_name(
        self,
        sensors: Iterable[Sensor[Any]],
    ) -> dict[str, Sensor[Any]]:
        by_name: dict[str, Sensor[Any]] = {}
        for sensor in sensors:
            if sensor.name in by_name:
                msg = MSG_DUBL_NAME.format(name=sensor.name)
                log.critical(msg)
                raise ValueError(msg)
            by_name[sensor.name] = sensor
        return by_name

    def __create_by_id(
        self,
        sensors: Iterable[Sensor[Any]],
    ) -> dict[int, Sensor[Any]]:
        by_id: dict[int, Sensor[Any]] = {}
        for sensor in sensors:
            if sensor.identificator in by_id:
                msg = MSG_DUBL_ID.format(id=sensor.identificator)
                log.critical(msg)
                raise ValueError(msg)
            by_id[sensor.identificator] = sensor
        return by_id
