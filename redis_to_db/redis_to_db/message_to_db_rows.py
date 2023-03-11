import logging

import arrow
from db.data.models import AggEnum, Row
from functools import singledispatch
from shared.messages import OpenCloseSensor
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
def _(msg: OpenCloseSensor) -> tuple[Row, ...]:
    return (
        Row(
            ts=arrow.now(),
            entity=msg.entity_id,
            attr="openess",
            value=float(msg.opened),
            agg=AggEnum.curr,
        ),
    )
