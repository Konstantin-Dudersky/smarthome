/*
Запустить сборку и загрузку образов:

docker buildx bake --builder builder -f docker-bake.hcl --push pi

Один образ:

docker buildx bake --builder builder -f docker-bake.hcl --push sh_db
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

target "base_python_image" {
    dockerfile = "shared/Dockerfile"
    args = {
        POETRY_VER = "${POETRY_VER}",
        PYTHON_VER = "${PYTHON_VER}"
    }
    platforms = PLATFORMS
}

target "sh_db" {
    dockerfile = "db/Dockerfile"
    tags = [ "${REPO}/smarthome/sh_db" ]
    args = {
        POSTGRE_VER = "${POSTGRE_VER}"
        TIMESCALEDB_VER = "${TIMESCALEDB_VER}"
    }
    platforms = PLATFORMS
}

target "sh_deconz_hub" {
    dockerfile = "deconz_hub/Dockerfile"
    tags = [ "${REPO}/smarthome/sh_deconz_hub" ]
    args = {
        DECONZ_VER="${DECONZ_VER}"
    }
    platforms = PLATFORMS
}

target "sh_driver_deconz" {
    contexts = {
        base_python_image = "target:base_python_image"
    }
    dockerfile = "driver_deconz/Dockerfile"
    tags = [ "${REPO}/smarthome/sh_driver_deconz" ]
    platforms = PLATFORMS
}

target "sh_grafana" {
    dockerfile = "grafana/Dockerfile"
    tags = [ "${REPO}/smarthome/sh_grafana" ]
    args = {
        GRAFANA = GRAFANA
    }
    platforms = PLATFORMS
}

target "sh_setup" {
    contexts = {
        base_python_image = "target:base_python_image"
    }
    dockerfile = "setup/Dockerfile"
    tags = [ "${REPO}/smarthome/sh_setup" ]
    platforms = PLATFORMS
}

target "sh_redis" {
    dockerfile = "redis/Dockerfile"
    tags = [ "${REPO}/smarthome/sh_redis" ]
    args = {
        REDIS = REDIS
    }
    platforms = PLATFORMS
}

target "sh_redis_to_db" {
    contexts = {
        base_python_image = "target:base_python_image"
    }
    dockerfile = "redis_to_db/Dockerfile"
    tags = [ "${REPO}/smarthome/sh_redis_to_db" ]
    platforms = PLATFORMS
}

group "pi" {
    targets = [
        "sh_db",
        "sh_deconz_hub",
        "sh_driver_deconz",
        "sh_grafana",
        "sh_redis",
        "sh_redis_to_db",
        "sh_setup",
    ]
}
