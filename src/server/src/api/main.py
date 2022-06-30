"""API main."""

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

import uvicorn
from uvicorn.server import Server


app = FastAPI()


@app.get("/")
async def index() -> str:
    """Сообщения."""
    return "123123123"


async def api_task() -> None:
    """Задача для запуска сервера api."""
    config = uvicorn.Config(app, port=8000, log_level="info")
    server: Server = uvicorn.Server(
        config
    )  # pyright: reportUnknownMemberType=false
    await server.serve()
