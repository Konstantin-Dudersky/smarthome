ARG POETRY_VER=1.2.2
ARG PYTHON_VER=3.10.8

FROM python:${PYTHON_VER}-bullseye AS sh_base_image

ENV PATH="/root/.local/bin:$PATH"
ARG POETRY_VER

WORKDIR /root/code/

# ошибки при установке arm64
RUN ln -s /usr/bin/dpkg-split /usr/sbin/dpkg-split
RUN ln -s /usr/bin/dpkg-deb /usr/sbin/dpkg-deb
RUN ln -s /bin/tar /usr/sbin/tar
RUN ln -s /bin/rm /usr/sbin/rm

RUN apt-get -y update \
    && apt-get upgrade -y \
    # system tools
    && apt-get install -y htop \
    # network tools
    iproute2 iputils-ping \
    # psycopg2 depends
    libpq-dev \
    # poetry depends
    python3-venv curl python3-dev build-essential

RUN curl -sSL https://install.python-poetry.org | python3 - --version $POETRY_VER -y
RUN poetry config virtualenvs.in-project false

CMD ["tail", "-f", "/dev/null"]

# debugpy
EXPOSE 5678
