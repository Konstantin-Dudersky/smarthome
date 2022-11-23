# setup

Скачать или обновить скрипты (выполнять из корневой папки проекта)

```sh
git clone https://github.com/Konstantin-Dudersky/setup.git setup_clone \
&& rm -rf setup_clone/.git \
&& rsync -va setup_clone/ setup \
&& rm -rf setup_clone
```
