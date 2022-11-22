Скрипты для установки/обновления.

## Установка

Загрузка кода

```sh
rsync -vhra . admin@target:/home/admin/code --include='**.gitignore' --exclude='/.git' --filter=':- .gitignore' --delete-after
```

Установка docker

Установка системных образов docker

```sh
docker compose --profile system up -d
```









## systemd

Для запуска systemd сервиса нужно задать задачу poe в файле pyproject.toml

```sh
[tool.poe.tasks]
systemd = {script = "src.systemd:main(service_name='<service_name>', description='<description>', work_dir_rel='<work_dir_rel>'"}
```

work_dir_rel - относительный путь к рабочей папке сервиса

После создания задачи генерацию файла можно запустить:

```sh
poetry run poe systemd
```


## angular

### сборка проекта

```sh
[tool.poe.tasks]
ng_build = {script = "src.ng_build:main(work_dir_relative='../client', project='client')"}
```

```sh
poetry run poe ng_build
```

### разворачивание проекта

## tauri

```sh
[tool.poe.tasks]
tauri_build = {script = "src.tauri_build:main(work_dir_relative='../client', project='client')"}
```

```sh
poetry run poe tauri_build
```
