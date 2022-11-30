"""Пользовательские исключения."""


class DataNotReceivedError(Exception):
    """Данные не получены."""


class BufferEmptyError(Exception):
    """В буфере нет данных."""
