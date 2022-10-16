ARG POETRY_VER=1.2.2
ARG PYTHON_VER=3.10.8

FROM --platform=amd64 python:${PYTHON_VER}-bullseye AS sh_base_image

ENV PATH="/root/.local/bin:$PATH"
ARG POETRY_VER

WORKDIR /root/code/

RUN apt-get update && \
    apt-get upgrade -y && \
    # system tools
    apt-get install -y htop && \
    # network tools
    apt-get install -y iproute2 iputils-ping && \
    # psycopg2 depends
    apt-get install -y libpq-dev && \
    # poetry depends
    apt-get install -y python3-venv curl python3-dev build-essential

RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VER
RUN poetry config virtualenvs.in-project false

# debugpy
EXPOSE 5678