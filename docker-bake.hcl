/*
Запустить сборку и загрузку образов:

docker buildx bake --builder builder -f docker-bake.hcl --push pi

Один образ:

docker buildx bake --builder builder -f docker-bake.hcl --push db
*/

// https://hub.docker.com/r/deconzcommunity/deconz/tags
DECONZ_VER = "2.21.00"

// https://hub.docker.com/r/grafana/grafana/tags
GRAFANA = "9.4.3"

// https://www.python.org/downloads/
PYTHON_VER = "3.11.2"

// https://github.com/python-poetry/poetry
POETRY_VER = "1.4.0"

// как TIMESCALEDB_VER
POSTGRE_VER = "15"

// https://hub.docker.com/r/redis/redis-stack/tags
REDIS = "7.0.6-RC7"

// https://hub.docker.com/r/timescale/timescaledb/tags?page=1&name=pg15
TIMESCALEDB_VER = "2.10.1"


REPO = "docker-registry:5000"

PLATFORMS = [
    "linux/amd64",
    "linux/arm64"
]

target "_base_python_image" {
    dockerfile = "shared/Dockerfile"
    args = {
        POETRY_VER = "${POETRY_VER}",
        PYTHON_VER = "${PYTHON_VER}"
    }
    platforms = PLATFORMS
}

target "db" {
    dockerfile = "db/Dockerfile"
    tags = [ "${REPO}/smarthome/db" ]
    args = {
        POSTGRE_VER = "${POSTGRE_VER}"
        TIMESCALEDB_VER = "${TIMESCALEDB_VER}"
    }
    platforms = PLATFORMS
}

target "deconz_hub" {
    dockerfile = "deconz_hub/Dockerfile"
    tags = [ "${REPO}/smarthome/deconz_hub" ]
    args = {
        DECONZ_VER="${DECONZ_VER}"
    }
    platforms = PLATFORMS
}

target "driver_deconz" {
    contexts = {
        base_python_image = "target:_base_python_image"
    }
    dockerfile = "driver_deconz/Dockerfile"
    tags = [ "${REPO}/smarthome/driver_deconz" ]
    platforms = PLATFORMS
}

target "grafana" {
    dockerfile = "grafana/Dockerfile"
    tags = [ "${REPO}/smarthome/grafana" ]
    args = {
        GRAFANA = GRAFANA
    }
    platforms = PLATFORMS
}

target "pgadmin" {
    dockerfile-inline = "FROM dpage/pgadmin4:latest"
    tags = [ "${REPO}/smarthome/pgadmin" ]
    platforms = PLATFORMS
}

target "portainer" {
    dockerfile-inline = "FROM portainer/portainer-ce:latest"
    tags = [ "${REPO}/smarthome/portainer" ]
    platforms = PLATFORMS
}

target "redis" {
    dockerfile = "redis/Dockerfile"
    tags = [ "${REPO}/smarthome/redis" ]
    args = {
        REDIS = REDIS
    }
    platforms = PLATFORMS
}

target "redis_to_db" {
    contexts = {
        base_python_image = "target:_base_python_image"
    }
    dockerfile = "redis_to_db/Dockerfile"
    tags = [ "${REPO}/smarthome/redis_to_db" ]
    platforms = PLATFORMS
}

target "setup" {
    contexts = {
        base_python_image = "target:_base_python_image"
    }
    dockerfile = "setup/Dockerfile"
    tags = [ "${REPO}/smarthome/setup" ]
    platforms = PLATFORMS
}

group "pi" {
    targets = [
        "db",
        "deconz_hub",
        "driver_deconz",
        "grafana",
        "pgadmin",
        "portainer",
        "redis",
        "redis_to_db",
        "setup",
    ]
}
