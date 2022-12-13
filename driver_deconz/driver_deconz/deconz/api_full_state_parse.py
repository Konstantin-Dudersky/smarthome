"""Парсим ответ от API на запрос о полном состоянии."""

import json
from typing import NamedTuple

from pydantic import BaseModel

from .sensors.base_sensor import BaseSensorModel


class _FullStateModel(BaseModel):
    """Модель ответа на запрос полного состояния."""

    sensors: dict[int, BaseSensorModel]


class _FullStateParsed(NamedTuple):
    uniqueid: str
    sensor_data: str


class ParseFullState(object):
    """Парсинг полного состояния системы.

    В сообщении содержится словарь всех датчиков системы, у которых разные
    модели данных. Поэтому модель _FullStateModel содержит только основные поля.
    """

    def __init__(self, full_state_str: str) -> None:
        """Парсинг полного состояния системы."""
        self.__full_state_str = full_state_str
        full_state: _FullStateModel = self.__parse_model(full_state_str)
        uniqueid_by_id: dict[int, str] = self.__construct_uniqueid_by_id(
            full_state,
        )
        self.__data_by_uniqueid: list[
            _FullStateParsed
        ] = self.__construct_data_by_uniqueid(
            full_state_str=full_state_str,
            uniqueid_by_id=uniqueid_by_id,
        )

    @property
    def data_by_uniqueid(self) -> list[_FullStateParsed]:
        """Данные по каждому датчику."""
        return self.__data_by_uniqueid

    def __parse_model(self, full_state_str: str) -> _FullStateModel:
        return _FullStateModel.parse_raw(full_state_str)

    def __construct_uniqueid_by_id(
        self,
        full_state: _FullStateModel,
    ) -> dict[int, str]:
        uniqueid_by_id: dict[int, str] = {}
        for sensor_id, sensor_data in full_state.sensors.items():
            uniqueid_by_id[sensor_id] = sensor_data.uniqueid
        return uniqueid_by_id

    def __construct_data_by_uniqueid(
        self,
        full_state_str: str,
        uniqueid_by_id: dict[int, str],
    ) -> list[_FullStateParsed]:
        uniqueid_vs_data: list[_FullStateParsed] = []
        full_state_dict = json.loads(full_state_str)
        for id_, uniqueid in uniqueid_by_id.items():
            uniqueid_vs_data.append(
                _FullStateParsed(
                    uniqueid=uniqueid,
                    sensor_data=full_state_dict["sensors"][str(id_)],
                ),
            )
        return uniqueid_vs_data
