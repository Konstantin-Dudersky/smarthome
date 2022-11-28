Обмен данными с deconz_hub

- сервис получает данные с сервиса `deconz_hub` по двум каналам:
  - websocket
  - HTTP REST API
- api для доступа к актуальному состоянию датчиков
- архивирование показаний в БД

## API KEY

Для доступа к `deconz_hub` необходимо сгенерировать API KEY.

- Выбрать в настройках веб-интерфейса **Authenticate app**
- Послать POST-запрос на адрес /api с телом:

```json
{
  "devicetype": "smarthome"
}
```

API key будет в ответе.

## Запуск

Для запуска в консоли:

```sh
poetry run python -m driver_deconz
```
