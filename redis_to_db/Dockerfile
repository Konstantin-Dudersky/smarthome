FROM base_python_image
# контекст - родительская папка
COPY . /root/code 
WORKDIR /root/code/redis_to_db
RUN poetry install --only main
CMD ["poetry", "run", "start"]
