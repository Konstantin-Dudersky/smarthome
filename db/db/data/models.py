"""Модели данных."""

from dataclasses import dataclass
from typing import Any, Self, Sequence

from psycopg import Cursor
from psycopg.rows import RowMaker as _RowMaker
from pydantic import BaseModel


@dataclass
class AggDistinct(BaseModel):
    """Строка в таблице."""

    entity: int
    attr: str
    agg: AggEnum
    aggnext: tuple[AggEnum, ...]

    @staticmethod
    def row_factory(cursor: Cursor[Any]) -> _RowMaker["AggDistinct"]:
        """Преобразование данных из БД.

        :param cursor: ссылка на курсор
        :return: функция для преобразования строк в объект Row
        """
        _: Cursor[Any] = cursor

        def make_row(values: Sequence[Any]) -> Self:
            aggnext_list: list[str] = (
                values[3]
                .decode("utf-8")
                .replace("{", "")
                .replace("}", "")
                .split(",")
            )
            return AggDistinct(
                entity=values[0],
                attr=values[1].decode("utf-8"),
                agg=AggEnum(values[2].decode("utf-8")),
                aggnext=tuple(AggEnum(a) for a in aggnext_list),
            )

        return make_row


@dataclass
class SingleVal(BaseModel):
    """Строка в таблице."""

    entity: int
    agg_value: float

    @staticmethod
    def row_factory(cursor: Cursor[Any]) -> _RowMaker["SingleVal"]:
        """Преобразование данных из БД.

        :param cursor: ссылка на курсор
        :return: функция для преобразования строк в объект SingleVal
        """
        _: Cursor[Any] = cursor

        def make_row(values: Sequence[Any]) -> Self:
            return SingleVal(
                entity=values[0],
                agg_value=values[1],
            )

        return make_row
