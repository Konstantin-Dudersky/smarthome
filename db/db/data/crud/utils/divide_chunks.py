"""Разделить список на части определенного размера."""

from typing import Generator, Sequence, TypeVar

TRowInChunk = TypeVar("TRowInChunk")


def divide_chunks(
    source_list: Sequence[TRowInChunk],
    chunk_size: int,
) -> Generator[tuple[TRowInChunk, ...], None, None]:
    """Разделить список на части определенного размера.

    В psycopg есть ограничение на кол-во параметров в одном запросе
    """
    for i in range(0, len(source_list), chunk_size):  # noqa: WPS526, WPS111
        yield tuple(source_list[i : i + chunk_size])
