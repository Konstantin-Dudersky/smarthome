# setup

Скачать или обновить скрипты (выполнять из корневой папки проекта)

```sh
git clone https://github.com/Konstantin-Dudersky/setup.git setup_clone \
&& rm -rf setup_clone/.git \
&& rsync -va setup_clone/ setup --ignore-existing \
&& rsync -va setup_clone/setup/ setup/setup \
&& rm -rf setup_clone
```

## Локальные задачи

Для добавления задач, требующих установки виртуального окружения, можно создать свой файл, и написать задачи в разделе `[tool.poetry.scripts]`.

- Создаем файл в папке `setup/setup/local_tasks.py`

```python
"""Скрипты для выполнения из виртуального окружения."""

import os
from pathlib import Path

from shared import settings


def create_env():
    path_str = "{current}/..".format(current=os.getcwd())
    path = Path(path_str).resolve()
    settings.create_env(
        work_dir_abs=path,
        profiles={settings.Prof.deconz_hub},
    )
```

- в файле `setup/pyproject.toml` в разделе `[tool.poetry.scripts]` описываем:

```toml
[tool.poetry.scripts]
create_env = "setup.local_tasks:create_env"
```

