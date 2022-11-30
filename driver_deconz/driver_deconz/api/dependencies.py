"""Конфигурирование зависимостей."""

from shared.fastapi import BaseDependencies

from ..deconz.sensors.sensors_collection import SensorCollection


class Dependencies(BaseDependencies):
    """Зависимости."""

    def __init__(
        self,
        sensors: SensorCollection,
    ) -> None:
        """Зависимости."""
        self.__sensors = sensors

    def sensors(self) -> SensorCollection:
        """Коллекция датчиков."""
        return self.__sensors

    @property
    def sensors_type(self):
        """Тип зависимости коллекции датчиков."""
        return SensorCollection
