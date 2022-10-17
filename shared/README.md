Общие модули для проекта

Документация проекта:

```sh
poetry run sphinx-apidoc --force -o docs/sphinx_in shared \
    && poetry run sphinx-build -b html docs/sphinx_in docs/sphinx_out
```

```
poetry run sphinx-apidoc --force -o sphinx/in ../shared


```
