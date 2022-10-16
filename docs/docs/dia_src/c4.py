from konstantin_docs.dia.c4 import (
    C4,
    component,
    container,
    context,
    rel,
    sprite,
)


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
zigbee = container.ContainerExt(
    label="Zigbee sensors",
    techn="T, P, ...",
    sprite=sprite.tupadr3.FontAwesome5(
        sprite.tupadr3.FontAwesome5Lib.THERMOMETER
    ),
)
yeelight = container.ContainerExt(
    label="Yeelight bulbs",
    techn="Yeelight",
    sprite=sprite.tupadr3.FontAwesome5(
        sprite.tupadr3.FontAwesome5Lib.LIGHTBULB
    ),
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
server_yeelight = component.Component(
    label="yeelight-service",
    techn="asyncio stream",
    sprite=sprite.tupadr3.Devicons(sprite.tupadr3.DeviconsLib.PYTHON),
)
server_telegram = component.Component(
    label="telegram-service",
    techn="telegram",
    sprite=sprite.tupadr3.Devicons(sprite.tupadr3.DeviconsLib.PYTHON),
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
    links_context=[
        smarthome := context.SystemBoundary(
            label="smarthome",
            links_container=[
                web_app,
                desktop_app,
                deconz_hub := container.ContainerExt(
                    label="deconz_hub",
                    techn="REST API, websockets",
                    sprite=sprite.tupadr3.FontAwesome5(
                        sprite.tupadr3.FontAwesome5Lib.SERVER
                    ),
                ),
                raspberry := container.ContainerBoundary(
                    label="raspberry",
                    links_component=[
                        api,
                        server_weather,
                        driver_deconz := component.Component(
                            label="driver_deconz",
                            techn="httpx, websockets",
                            sprite=sprite.tupadr3.Devicons(
                                sprite.tupadr3.DeviconsLib.PYTHON
                            ),
                        ),
                        server_db := component.ComponentDb(
                            label="db",
                            techn="PostgreSQL+TimescaleDB",
                            descr="Настройки, архивы",
                            sprite=sprite.tupadr3.Devicons(
                                sprite.tupadr3.DeviconsLib.POSTGRESQL
                            ),
                        ),
                        server_yeelight,
                        server_telegram,
                    ],
                ),
                zigbee,
                yeelight,
            ],
        ),
        weather,
        telegram,
    ],
    links_rel=[
        rel.Rel(label="Uses", links=(web_app, api), techn="http"),
        rel.Rel(label="Uses", links=(desktop_app, api), techn="http"),
        rel.RelBack(
            label="Uses", links=(weather, server_weather), techn="http"
        ),
        rel.BiRel(
            label="Uses", links=(driver_deconz, deconz_hub), techn="http"
        ),
        rel.Rel(label="Uses", links=(deconz_hub, zigbee), techn="zigbee"),
        rel.Rel(
            label="R/W",
            links=(server_yeelight, yeelight),
            techn="http,Wi-Fi",
        ),
        rel.RelBack(
            label="send",
            links=(telegram, server_telegram),
            techn="http",
        ),
    ],
)
