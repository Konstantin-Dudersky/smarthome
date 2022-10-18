FROM sh_base_image AS sh_driver_deconz
# контекст - родительская папка
COPY . /root/code 
WORKDIR /root/code/driver_deconz
RUN poetry update --lock --only main \
    && poetry install --only main \
    && poetry show -o
