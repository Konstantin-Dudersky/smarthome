"""Задача для хостинга api."""

import uvicorn

from .main import app


async def api_task(port: int = 8000) -> None:
    """Задача для запуска сервера api."""
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info",
    )
    server = uvicorn.Server(
        config,
    )  # pyright: reportUnknownMemberType=false
    await server.serve()
