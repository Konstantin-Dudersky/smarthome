"""Работа с TimescaleDB."""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any, Final, Sequence

from psycopg import Cursor
from psycopg.rows import RowMaker as _RowMaker

from typing_extensions import Self


class AggEnum(Enum):
    """Типы аггрегации."""

    CURR = "curr"
    FIRST = "first"
    INC = "inc"
    SUM = "sum"
    MEAN = "mean"
    MIN = "min"
    MAX = "max"


class AttrElectricCounterEnum(Enum):
    """Значения атрибутов для электрических счетчиков."""

    EP_IN = "ep_in"
    EP_IN_T1 = "ep_in_t1"
    EP_IN_T2 = "ep_in_t2"
    EP_IN_T3 = "ep_in_t3"
    EP_IN_T4 = "ep_in_t4"
    EP_OUT = "ep_out"
    EP_OUT_T1 = "ep_out_t1"
    EP_OUT_T2 = "ep_out_t2"
    EP_OUT_T3 = "ep_out_t3"
    EP_OUT_T4 = "ep_out_t4"
    EQ_IN = "eq_in"
    EQ_IN_T1 = "eq_in_t1"
    EQ_IN_T2 = "eq_in_t2"
    EQ_IN_T3 = "eq_in_t3"
    EQ_IN_T4 = "eq_in_t4"
    EQ_OUT = "eq_out"
    EQ_OUT_T1 = "eq_out_t1"
    EQ_OUT_T2 = "eq_out_t2"
    EQ_OUT_T3 = "eq_out_t3"
    EQ_OUT_T4 = "eq_out_t4"
    F = "f"
    F1 = "f1"
    F2 = "f2"
    F3 = "f3"
    I = "i"
    I1 = "i1"
    I2 = "i2"
    I3 = "i3"
    P = "p"
    P1 = "p1"
    P2 = "p2"
    P3 = "p3"
    P_IN = "p_in"
    P_IN_T1 = "p_in_t1"
    P_IN_T2 = "p_in_t2"
    P_IN_T3 = "p_in_t3"
    P_IN_T4 = "p_in_t4"
    P_OUT = "p_out"
    P_OUT_T1 = "p_out_t1"
    P_OUT_T2 = "p_out_t2"
    P_OUT_T3 = "p_out_t3"
    P_OUT_T4 = "p_out_t4"
    PF = "pf"
    PF1 = "pf1"
    PF2 = "pf2"
    PF3 = "pf3"
    Q = "q"
    Q1 = "q1"
    Q2 = "q2"
    Q3 = "q3"
    Q_IN = "q_in"
    Q_IN_T1 = "q_in_t1"
    Q_IN_T2 = "q_in_t2"
    Q_IN_T3 = "q_in_t3"
    Q_IN_T4 = "q_in_t4"
    Q_OUT = "q_out"
    Q_OUT_T1 = "q_out_t1"
    Q_OUT_T2 = "q_out_t2"
    Q_OUT_T3 = "q_out_t3"
    Q_OUT_T4 = "q_out_t4"
    S = "s"
    S1 = "s1"
    S2 = "s2"
    S3 = "s3"
    U = "u"
    U1 = "u1"
    U2 = "u2"
    U3 = "u3"


class StatusEnum(Enum):
    """Коды статуса."""

    GOOD = "Good"
    UNCERTAIN = "Uncertain"
    BAD = "Bad"


@dataclass
class BaseModel(ABC):
    """Базовый класс для строк."""

    @staticmethod
    @abstractmethod
    def row_factory(cursor: Cursor[Any]) -> _RowMaker["BaseModel"]:
        """Преобразование данных из БД.

        :param cursor: ссылка на курсор
        :return: функция для преобразования строк в объект Row
        """


@dataclass
class Row(BaseModel):
    """Строка в таблице."""

    ts: datetime
    entity: int
    attr: str
    value: float | None
    status: StatusEnum
    agg: AggEnum
    aggts: datetime | None
    aggnext: tuple[AggEnum, ...] | None  # noqa

    num_params: Final[int] = 8

    @property
    def execute_query(self: Self) -> str:
        """Для вставки в параметр query инструкции execute.

        :return: строка для вставки
        """
        return "(%s, %s, %s, %s, %s, %s, %s, %s)"

    @property
    def execute_params(
        self: Self,
    ) -> tuple[
        datetime,
        int,
        str,
        float | None,
        str,
        str,
        datetime | None,
        list[str] | None,
    ]:
        """Для вставки в параметр params инструкции execute.

        :return: кортеж для добавления параметров
        """
        if self.aggnext is None:
            aggnext = None
        else:
            aggnext = [a.value for a in self.aggnext]
        return (
            self.ts,
            self.entity,
            self.attr,
            self.value,
            self.status.value,
            self.agg.value,
            self.aggts,
            aggnext,
        )

    @staticmethod
    def row_factory(cursor: Cursor[Any]) -> _RowMaker["Row"]:
        """Преобразование данных из БД.

        :param cursor: ссылка на курсор
        :return: функция для преобразования строк в объект Row
        """
        _: Cursor[Any] = cursor

        def make_row(values: Sequence[Any]) -> "Row":
            aggnext: tuple[AggEnum, ...] | None = None
            if values[7] is not None:
                aggnext_list: list[str] = (
                    values[7]
                    .decode("utf-8")
                    .replace("{", "")
                    .replace("}", "")
                    .split(",")
                )
                aggnext = tuple(AggEnum(a) for a in aggnext_list)
            return Row(
                ts=values[0],
                entity=values[1],
                attr=values[2],
                value=values[3],
                status=StatusEnum(values[4]),
                agg=AggEnum(values[5]),
                aggts=values[6],
                aggnext=aggnext,
            )

        return make_row


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
