FROM base_python_image
# контекст - родительская папка
COPY . /root/code 
WORKDIR /root/code/driver_deconz
RUN poetry install --only main
CMD ["poetry", "run", "start"]
