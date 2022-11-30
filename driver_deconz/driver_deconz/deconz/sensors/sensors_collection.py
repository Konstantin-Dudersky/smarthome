"""Коллекция датчиков.

К отдельным датчикам можно обращаться как по id, так и по имени name.
"""

import logging
from typing import Any, Final, Iterable

from shared.patterns import SingletonMeta

from .base_sensor import BaseSensor

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

MSG_DUBL_NAME: Final[str] = "Повторяющееся название датчика: {name}"
MSG_DUBL_ID: Final[str] = "Повторяющийся id датчика: {id}"

UNKNOWN_NAME: Final[str] = "Неизвестное название: {name}"
UNKNOWN_ID: Final[str] = "Неизвестный идентификатор: {id}"


TCollection = dict[str, BaseSensor[Any]]


class SensorCollection(object, metaclass=SingletonMeta["SensorCollection"]):
    """Коллеция датчиков."""

    def __init__(
        self,
        sensors: Iterable[BaseSensor[Any]],
    ) -> None:
        """Коллеция датчиков."""
        self.__by_uniqueid: TCollection = self.__view_by_uniqueid(sensors)
        self.__by_name: TCollection = self.__view_by_name(sensors)
        log.debug("Created sensor collection:\n{0}".format(self.__by_name))

    def by_id(self, identificator: str) -> BaseSensor[Any]:
        """Датчик по идентификатору."""
        if identificator not in self.__by_uniqueid:
            msg = UNKNOWN_ID.format(id=identificator)
            log.warning(msg)
            raise ValueError(msg)
        return self.__by_uniqueid[identificator]

    def by_name(self, name: str) -> BaseSensor[Any]:
        """Датчик по названию."""
        if name not in self.__by_name:
            msg = UNKNOWN_NAME.format(name=name)
            log.warning(msg)
            raise ValueError(msg)
        return self.__by_name[name]

    @property
    def all_by_name(self) -> TCollection:
        """Словарь всех датчиков."""
        return self.__by_name

    def __view_by_name(
        self,
        sensors: Iterable[BaseSensor[Any]],
    ) -> TCollection:
        by_name: TCollection = {}
        for sensor in sensors:
            if sensor.name in by_name:
                msg = MSG_DUBL_NAME.format(name=sensor.name)
                log.critical(msg)
                raise ValueError(msg)
            by_name[sensor.name] = sensor
        return by_name

    def __view_by_uniqueid(
        self,
        sensors: Iterable[BaseSensor[Any]],
    ) -> TCollection:
        by_id: TCollection = {}
        for sensor in sensors:
            if sensor.uniqueid in by_id:
                msg = MSG_DUBL_ID.format(id=sensor.uniqueid)
                log.critical(msg)
                raise ValueError(msg)
            by_id[sensor.uniqueid] = sensor
        return by_id
