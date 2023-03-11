import logging

import arrow
from db.data.models import AggEnum, Row
from functools import singledispatch
from shared import messages
from typing import Final

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

MSG: Final[str] = "Неизвестное сообщение, невозможно сохранить в БД:\n{msg}"


class UnknownMessage(Exception):
    pass


@singledispatch
def message_to_db_rows(msg: object) -> tuple[Row, ...]:
    log_msg = MSG.format(msg=msg)
    log.error(log_msg)
    raise UnknownMessage(log_msg)


@message_to_db_rows.register
def _(msg: messages.OpenCloseSensor) -> tuple[Row, ...]:
    return (
        Row(
            ts=arrow.Arrow.fromdatetime(msg.ts),
            entity=msg.entity_id,
            attr="openess",
            value=float(msg.opened),
            agg=AggEnum.curr,
        ),
    )


@message_to_db_rows.register
def _(msg: messages.TemperatureSensor) -> tuple[Row, ...]:
    return (
        Row(
            ts=arrow.Arrow.fromdatetime(msg.ts),
            entity=msg.entity_id,
            attr="temperature",
            value=msg.temperature,
            agg=AggEnum.curr,
        ),
    )
