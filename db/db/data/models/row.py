"""Модель для строки в БД."""

import arrow
from pydantic import BaseConfig, BaseModel, validator

from .enums import AggEnum, StatusEnum


class Row(BaseModel):
    """Строка в таблице."""

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

    @validator("aggnext", pre=True)
    def validate_aggnext(
        cls,  # noqa: N805
        aggnext: str | tuple[AggEnum] | None,
    ) -> tuple[AggEnum, ...] | None:
        """Валидация aggnext.

        Возможно, баг в psycopg - при чтении из БД вместо списка возвращается
        строка, обернутая фигурными скобками: {item1, item2, ...}
        """
        if aggnext is None:
            return None
        if isinstance(aggnext, tuple):
            return aggnext
        aggnext_list: tuple[str] = tuple(
            aggnext.replace("{", "").replace("}", "").split(","),
        )
        return tuple(AggEnum(agg) for agg in aggnext_list)

    @property
    def execute_query(self) -> str:
        """Для вставки в параметр query инструкции execute."""
        return "(%s, %s, %s, %s, %s, %s, %s, %s)"

    @property
    def execute_params(
        self,
    ) -> tuple[
        arrow.Arrow,
        int,
        str,
        float | None,
        StatusEnum,
        AggEnum,
        arrow.Arrow | None,
        list[AggEnum] | None,
    ]:
        """Для вставки в параметр params инструкции execute."""
        return (
            self.ts,
            self.entity,
            self.attr,
            self.value,
            self.status,
            self.agg,
            self.aggts,
            list(self.aggnext) if self.aggnext else None,
        )
