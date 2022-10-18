Документация проекта

## Генерация документации пакетов python

Запуск генерации из вирт. окружения docs

```sh
poetry run poe sphinx
```

Вместо выполнения команды в терминеле можно запустить задачу `sphinx` vscode.

### Добавить новый пакет для генерации:

- добавить зависимость в файле `pyproject.toml` проекта `docs`, обновить пакеты:

```toml
__package_name__ = { path = "../__package_name__", develop = true }
```

- обновить команду генерации в файле `pyproject.toml` проекта `docs`, секция `tool.poe.tasks.sphinx`:

```sh
poetry run sphinx-apidoc --force --separate -o sphinx/in ../__package_name__
```

- добавить ссылку на пакет в файле `sphinx/in/index.rst`


## Генерация документации webapp

