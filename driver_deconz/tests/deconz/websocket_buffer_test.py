import pytest

from driver_deconz.deconz.websocket_buffer import (
    WebsocketBuffer,
    WebsocketBufferItem,
)
from driver_deconz.deconz.exceptions import BufferEmptyError


@pytest.fixture
def buffer() -> WebsocketBuffer:
    return WebsocketBuffer()


def test_get_empty_buffer(buffer: WebsocketBuffer) -> None:
    with pytest.raises(BufferEmptyError):
        buffer.get()


def test_buffer_put(buffer: WebsocketBuffer) -> None:
    msg = WebsocketBufferItem(
        uniqueid="1",
        state="2",
    )
    buffer.put(msg)
    assert msg == buffer.get()
