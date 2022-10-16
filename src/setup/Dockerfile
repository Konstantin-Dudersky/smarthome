FROM sh_base_image AS sh_setup
# контекст - родительская папка
COPY . /root/code 
WORKDIR /root/code/setup
RUN poetry update --lock \
    && poetry install --only main \
    && poetry show -o
