from konstantin_docs.dia.c4 import C4, component, container, context, rel, sprite


web_app = container.Container(
    label="web app",
    techn="angular",
    sprite=sprite.tupadr3.Devicons(sprite.tupadr3.DeviconsLib.ANGULAR),
)
desktop_app = container.Container(
    label="desktop app",
    techn="angular, tauri",
    sprite=sprite.tupadr3.Devicons(sprite.tupadr3.DeviconsLib.ANGULAR),
)
deconz = container.ContainerExt(
    label="Deconz",
    techn="REST API, websockets",
    sprite=sprite.tupadr3.FontAwesome5(sprite.tupadr3.FontAwesome5Lib.SERVER),
)
zigbee = container.ContainerExt(
    label="Zigbee sensors",
    techn="T, P, ...",
    sprite=sprite.tupadr3.FontAwesome5(sprite.tupadr3.FontAwesome5Lib.THERMOMETER),
)
yeelight = container.ContainerExt(
    label="Yeelight bulbs",
    techn="Yeelight",
    sprite=sprite.tupadr3.FontAwesome5(sprite.tupadr3.FontAwesome5Lib.LIGHTBULB),
)
# server app
api = component.Component(
    label="API",
    techn="FastAPI",
    sprite=sprite.tupadr3.Devicons(sprite.tupadr3.DeviconsLib.PYTHON),
)
server_weather = component.Component(
    label="weather-service",
    techn="Python",
    sprite=sprite.tupadr3.Devicons(sprite.tupadr3.DeviconsLib.PYTHON),
)
server_deconz = component.Component(
    label="deconz-service",
    techn="httpx, websockets",
    sprite=sprite.tupadr3.Devicons(sprite.tupadr3.DeviconsLib.PYTHON),
)
server_yeelight = component.Component(
    label="yeelight-service",
    techn="asyncio stream",
    sprite=sprite.tupadr3.Devicons(sprite.tupadr3.DeviconsLib.PYTHON),
)
server_db = component.ComponentDb(
    label="DB",
    techn="SQLite",
    descr="Для сохранения состояния и настроек",
    sprite=sprite.tupadr3.Devicons(sprite.tupadr3.DeviconsLib.SQLLITE),
)
server_telegram = component.Component(
    label="telegram-service",
    techn="telegram",
    sprite=sprite.tupadr3.Devicons(sprite.tupadr3.DeviconsLib.PYTHON),
)
server = container.ContainerBoundary(
    label="Server",
    links_component=[api, server_weather, server_deconz, server_db, server_yeelight, server_telegram],
)

db = container.ContainerDb(
    label="DB",
    techn="PostgreSQL+TimescaleDB",
    descr="Для архивов",
    sprite=sprite.tupadr3.Devicons(sprite.tupadr3.DeviconsLib.POSTGRESQL),
)

smarthome = context.SystemBoundary(
    label="smarthome",
    links_container=[web_app, desktop_app, deconz, server, db, zigbee, yeelight],
)
weather = context.SystemExt(
    label="Weather",
    sprite=sprite.tupadr3.FontAwesome5(sprite.tupadr3.FontAwesome5Lib.SUN),
)
telegram = context.SystemExt(
    label="Telegram",
    sprite=sprite.tupadr3.FontAwesome5(sprite.tupadr3.FontAwesome5Lib.TELEGRAM),
)

dia = C4(
    filename="c4",
    title="C4",
    links_context=[smarthome, weather, telegram],
    links_rel=[
        rel.Rel(label="Uses", links=(web_app, api), techn="http"),
        rel.Rel(label="Uses", links=(desktop_app, api), techn="http"),
        rel.RelBack(label="Uses", links=(weather, server_weather), techn="http"),
        rel.Rel(label="Uses", links=(server_deconz, deconz), techn="http"),
        rel.Rel(label="Uses", links=(deconz, zigbee), techn="zigbee"),
        rel.Rel(label="R/W", links=(server, db), techn="sqlalchemy+psycopg"),
        rel.Rel(label="R/W", links=(server_yeelight, yeelight), techn="http,Wi-Fi"),
        rel.RelBack(label="send", links=(telegram, server_telegram), techn="http"),
    ],
)
