"""API main."""

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

import uvicorn
from uvicorn.server import Server

from src.utils.logger import LoggerLevel, get_logger

from .api_devices import router as devices_router

log = get_logger(__name__, LoggerLevel.INFO)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(devices_router)


@app.exception_handler(
    RequestValidationError,
)  # pyright: reportUntypedFunctionDecorator=false
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    """Логгирование неправильных запросов.

    :param request: запрос
    :param exc: исключение
    :return: json с перечнем ошибок
    """
    log.error(
        "Неправильный запрос.\n-> Запрос: %s\n-> Ошибки: %s",
        request.url,
        exc.errors(),
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


# ------------------------------------------------------------------------------
# angular app - должно быть в конце


@app.get("/")
def index() -> HTMLResponse:
    """Веб-приложение.

    :return: index.html
    """
    with open("static/index.html", "r", encoding="utf-8") as file_index:
        html_content = file_index.read()
    return HTMLResponse(html_content, status_code=200)


app.mount("/", StaticFiles(directory="static"), name="static")

# ------------------------------------------------------------------------------


async def api_task() -> None:
    """Задача для запуска сервера api."""
    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="warning",
    )
    server: Server = uvicorn.Server(
        config,
    )  # pyright: reportUnknownMemberType=false
    await server.serve()
