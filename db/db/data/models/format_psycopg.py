"""Форматирование словаря параметров для вставки в запрос psycopg.

https://www.psycopg.org/psycopg3/docs/basic/params.html
"""

from typing import Any

TKey = str
TValue = Any
TDict = dict[TKey, TValue]


class FormatPsycopg(object):
    """Форматирование словаря параметров для вставки в запрос psycopg."""

    def __init__(self, model_dict: TDict) -> None:
        """Форматирование словаря параметров для вставки в запрос psycopg."""
        self.__model_dict: TDict

        self.__model_dict = model_dict

    @property
    def query(self) -> str:
        """Для вставки в тело запроса."""
        single_key = ["%s"]  # noqa: WPS323
        keys = single_key * len(self.__model_dict)
        keys_joined = ",".join(keys)
        return "({0})".format(keys_joined)

    @property
    def params(self) -> list[TValue]:  # noqa: WPS110
        """Для вставки в перечень параметров запроса."""
        return list(self.__model_dict.values())
