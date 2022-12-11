from typing import Any
from db.data.models.format_psycopg import FormatPsycopg
from db.data.models.enums import StatusEnum

model_data: dict[str, Any] = {
    "name": "test_name",
    "value": 123,
    "status": StatusEnum.bad,
    "aggts": None,
}


def test_for_query() -> None:
    query = "(%s,%s,%s,%s)"
    assert FormatPsycopg(model_data).query == query


def test_for_params() -> None:
    params = [
        "test_name",
        123,
        StatusEnum.bad,
        None,
    ]
    assert FormatPsycopg(model_data).params == params
