FROM sh_base_image AS sh_driver_deconz
# контекст - родительская папка
COPY . /root/code 
WORKDIR /root/code/driver_deconz
RUN poetry install --only main
