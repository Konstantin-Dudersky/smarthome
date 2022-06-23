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
# core app
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
    techn="aiohttp",
    sprite=sprite.tupadr3.Devicons(sprite.tupadr3.DeviconsLib.PYTHON),
)
server_db = component.ComponentDb(
    label="DB",
    techn="SQLite",
    descr="Для сохранения состояния и настроек",
    sprite=sprite.tupadr3.Devicons(sprite.tupadr3.DeviconsLib.SQLLITE),
)
server = container.ContainerBoundary(
    label="Server",
    links_component=[api, server_weather, server_deconz, server_db],
)

db = container.ContainerDb(
    label="DB",
    techn="PostgreSQL+TimescaleDB",
    descr="Для архивов",
    sprite=sprite.tupadr3.Devicons(sprite.tupadr3.DeviconsLib.POSTGRESQL),
)

smarthome = context.SystemBoundary(
    label="smarthome",
    links_container=[web_app, desktop_app, deconz, server, db, zigbee],
)
weather = context.SystemExt(
    label="Weather",
    sprite=sprite.tupadr3.FontAwesome5(sprite.tupadr3.FontAwesome5Lib.SUN),
)

dia = C4(
    filename="c4",
    title="C4",
    links_context=[smarthome, weather],
    links_rel=[
        rel.Rel(label="Uses", links=(web_app, api), techn="http"),
        rel.Rel(label="Uses", links=(desktop_app, api), techn="http"),
        rel.Rel(label="Uses", links=(server_weather, weather), techn="http"),
        rel.Rel(label="Uses", links=(server_deconz, deconz), techn="http"),
        rel.Rel(label="Uses", links=(deconz, zigbee), techn="zigbee"),
        rel.Rel(label="R/W", links=(server, db), techn="sqlalchemy+psycopg"),
    ],
)
