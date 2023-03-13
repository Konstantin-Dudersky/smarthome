Управление автоматикой в доме.

## Описание

Структурная схема:

![docs/diagrams/out/c4.svg](docs/diagrams/out/c4.svg)

Сервисы:

| Сервис                                   | Описание                                      | Запуск зависит от |
| ---------------------------------------- | --------------------------------------------- | ----------------- |
| [db](db/README.md)                       | База данных PostgreSQL                        |                   |
| deconz_hub                               |                                               |                   |
| [driver_deconz](driver_deconz/README.md) | Считывание Zegbee датчиков и передача в Redis | deconz_hub, redis |
| driver_yeelight                          |                                               | redis             |
| grafana                                  | Просмотр исторических данных                  | db, redis         |
| pgadmin                                  | Веб-интерфейс для управления db               |                   |
| portainer                                | Веб-интерфейс для docker                      |                   |
| redis                                    | Брокер сообщений                              |                   |
| [redis_to_db](redis_to_db/README.md)     | Архивация сообщений из брокера                | db, redis         |
|                                          |                                               |                   |

Документацию можно смотреть в [obsidian](https://obsidian.md/). Открыть корневую папку репозитория (open folder as vault). Затем можно открывать по ярлыку `obsidian.py`.

## Установка

### Установка ОС

Операционная система - Raspbian. Образ удобно записывать raspberry imager. При создании образа активировать доступ по SSH, задать пользователя.

После установки командой sudo raspi-config открыть доступ по VNC. Подключиться можно через VNC-клиент [realvnc](https://www.realvnc.com/en/connect/download/viewer/).

### Установка ПО

Копируем проект на целевую систему

```bash
./run.py codesync
```

Сервисы:

- sh_db - [db/README](db/README.md)
- portainer - https://

### Запуск

```bash
docker compose --profile pi pull
docker compose --profile pi up -d
```

### Документация

Ссылки:

- исходный код python - [sphinx](docs/sphinx/out/index.html)

Подробнее о генерации - [docs/README](docs/README.md)
