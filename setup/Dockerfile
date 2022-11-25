FROM base_python_image
# контекст - родительская папка
COPY . /root/code 
WORKDIR /root/code/setup
RUN poetry install --only main
