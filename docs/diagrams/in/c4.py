from dataclass_to_diagram.models import c4

dia = c4.C4(
    contexts=[
        smarthome := c4.context.SystemBoundary(
            label="smarthome",
            containers=[
                web_app := c4.container.Container(
                    label="web app",
                    techn="angular",
                    sprite=c4.sprite.tupadr3.Devicons(
                        c4.sprite.tupadr3.Devicons.angular
                    ),
                ),
                desktop_app := c4.container.Container(
                    label="desktop app",
                    techn="angular, tauri",
                    sprite=c4.sprite.tupadr3.Devicons(
                        c4.sprite.tupadr3.Devicons.angular
                    ),
                ),
                raspberry := c4.container.ContainerBoundary(
                    label="raspberry",
                    components=[
                        api := c4.component.Component(
                            label="API",
                            techn="FastAPI",
                            sprite=c4.sprite.tupadr3.Devicons(
                                c4.sprite.tupadr3.Devicons.python
                            ),
                        ),
                        server_weather := c4.component.Component(
                            label="weather-service",
                            techn="Python",
                            sprite=c4.sprite.tupadr3.Devicons(
                                c4.sprite.tupadr3.Devicons.python
                            ),
                        ),
                        db := c4.component.ComponentDb(
                            label="db",
                            techn="PostgreSQL+TimescaleDB",
                            descr="Настройки, архивы",
                            sprite=c4.sprite.tupadr3.Devicons(
                                c4.sprite.tupadr3.Devicons.postgresql
                            ),
                        ),
                        deconz_hub := c4.component.ComponentExt(
                            label="deconz_hub",
                            techn="REST API, websockets",
                            sprite=c4.sprite.tupadr3.FontAwesome5(
                                c4.sprite.tupadr3.FontAwesome5.server
                            ),
                        ),
                        driver_deconz := c4.component.Component(
                            label="driver_deconz",
                            techn="httpx, websockets",
                            sprite=c4.sprite.tupadr3.Devicons(
                                c4.sprite.tupadr3.Devicons.python
                            ),
                        ),
                        driver_yeelight := c4.component.Component(
                            label="driver_yeelight",
                            techn="asyncio stream",
                            sprite=c4.sprite.tupadr3.Devicons(
                                c4.sprite.tupadr3.Devicons.python
                            ),
                        ),
                        grafana := c4.component.Component(
                            label="grafana",
                            techn="grafana",
                        ),
                        pgadmin := c4.component.Component(
                            label="pgadmin",
                            techn="pgadmin",
                        ),
                        portainer := c4.component.Component(
                            label="portainer",
                            techn="portainer",
                            sprite=c4.sprite.tupadr3.Devicons(
                                c4.sprite.tupadr3.Devicons.docker
                            ),
                        ),
                        redis := c4.component.ComponentQueueExt(
                            label="redis",
                            techn="redis",
                            sprite=c4.sprite.tupadr3.Devicons(
                                c4.sprite.tupadr3.Devicons.redis
                            ),
                        ),
                        redis_to_db := c4.component.ComponentQueue(
                            label="redis_to_db",
                            techn="python",
                            sprite=c4.sprite.tupadr3.Devicons(
                                c4.sprite.tupadr3.Devicons.python
                            ),
                        ),
                        telegram := c4.component.Component(
                            label="telegram-service",
                            techn="telegram",
                            sprite=c4.sprite.tupadr3.Devicons(
                                c4.sprite.tupadr3.Devicons.python
                            ),
                        ),
                    ],
                ),
                zigbee := c4.container.ContainerExt(
                    label="Zigbee sensors",
                    techn="T, P, ...",
                    sprite=c4.sprite.tupadr3.FontAwesome5(
                        c4.sprite.tupadr3.FontAwesome5.thermometer
                    ),
                ),
                yeelight_bulbs := c4.container.ContainerExt(
                    label="Yeelight bulbs",
                    techn="Yeelight",
                    sprite=c4.sprite.tupadr3.FontAwesome5(
                        c4.sprite.tupadr3.FontAwesome5.lightbulb
                    ),
                ),
            ],
        ),
        weather := c4.context.SystemExt(
            label="Weather",
            sprite=c4.sprite.tupadr3.FontAwesome5(
                c4.sprite.tupadr3.FontAwesome5.sun
            ),
        ),
        telegram := c4.context.SystemExt(
            label="Telegram",
            sprite=c4.sprite.tupadr3.FontAwesome5(
                c4.sprite.tupadr3.FontAwesome5.telegram
            ),
        ),
    ],
    relations=[
        c4.rel.Rel(label="Uses", begin=web_app, end=api, techn="http"),
        c4.rel.Rel(label="Uses", begin=desktop_app, end=api, techn="http"),
        c4.rel.RelBack(
            label="Uses", begin=weather, end=server_weather, techn="http"
        ),
        c4.rel.BiRel(
            label="Uses", begin=driver_deconz, end=deconz_hub, techn="http, ws"
        ),
        c4.rel.Rel(label="Uses", begin=deconz_hub, end=zigbee, techn="zigbee"),
        c4.rel.Rel(
            label="R/W",
            begin=driver_yeelight,
            end=yeelight_bulbs,
            techn="http,Wi-Fi",
        ),
        c4.rel.RelBack(
            label="send",
            begin=telegram,
            end=telegram,
            techn="http",
        ),
        c4.rel.BiRel(begin=redis, end=driver_yeelight, label="r/w"),
        c4.rel.RelBack(begin=redis, end=driver_deconz, label="send"),
        c4.rel.RelRight(begin=redis_to_db, end=redis, label="read"),
        c4.rel.RelLeft(begin=redis_to_db, end=db, label="write"),
        c4.rel.Rel(begin=grafana, end=db, label="read"),
        c4.rel.Rel(begin=grafana, end=redis, label="read"),
        c4.rel.Rel(begin=pgadmin, end=db, label="control"),
    ],
)
