"""Модель для строки в БД."""

from typing import ClassVar

import arrow
from pydantic import BaseConfig, BaseModel, validator

from .enums import AggEnum, StatusEnum
from .format_psycopg import FormatPsycopg


class Row(BaseModel):
    """Модель для строки в БД."""

    class Config(BaseConfig):
        """Конфигурация."""

        arbitrary_types_allowed = True

    ts: arrow.Arrow
    entity: int
    attr: str
    value: float | None  # noqa: WPS110
    status: StatusEnum
    agg: AggEnum
    aggts: arrow.Arrow | None = None
    aggnext: tuple[AggEnum, ...] | None = None

    num_of_fields: ClassVar[int] = 8

    @validator("aggnext", pre=True)
    def validate_aggnext(
        cls,  # noqa: N805
        aggnext: str | tuple[AggEnum] | None,
    ) -> tuple[AggEnum, ...] | None:
        """Валидация aggnext.

        Возможно, баг в psycopg - при чтении из БД вместо списка возвращается
        строка, обернутая фигурными скобками: {item1, item2, ...}
        """
        match aggnext:
            case tuple():
                return aggnext
            case str():
                aggnext_str: list[str] = (
                    aggnext.replace("{", "").replace("}", "").split(",")
                )
                aggnext_enum: list[AggEnum] = [
                    AggEnum(agg) for agg in aggnext_str
                ]
                return tuple(aggnext_enum)
            case None:
                return None
            case _:
                raise ValueError(
                    "Unknown type of aggnext: {0}".format(type(aggnext)),
                )

    @property
    def format_psycopg(self) -> FormatPsycopg:
        """Форматирование данных модели для вставки в зарос psycopg."""
        dict_query_params = {
            "ts": self.ts,
            "entity": self.entity,
            "attr": self.attr,
            "value": self.value,
            "status": self.status,
            "agg": self.agg,
            "aggts": self.aggts,
            "aggnext": list(self.aggnext) if self.aggnext else None,
        }
        return FormatPsycopg(dict_query_params)
