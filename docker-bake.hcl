/*
Запустить сборку и загрузку образов:

docker buildx bake --builder builder -f docker-bake.hcl --push pi
*/

PYTHON_VER = "3.11.1" // https://www.python.org/downloads/
POETRY_VER = "1.3.0" // https://github.com/python-poetry/poetry
POSTGRE_VER = "14.6" // https://hub.docker.com/r/timescale/timescaledb-ha/tags
TIMESCALEDB_VER = "2.8.1"
DECONZ_VER = "2.19.03" // https://hub.docker.com/r/deconzcommunity/deconz/tags

REPO = "localhost:5000"

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

target "sh_setup" {
    contexts = {
        base_python_image = "target:base_python_image"
    }
    dockerfile = "setup/Dockerfile"
    tags = [ "${REPO}/smarthome/sh_setup" ]
    platforms = PLATFORMS
}

group "pi" {
    targets = [
        "sh_db", 
        "sh_deconz_hub", 
        "sh_driver_deconz", 
        "sh_setup", 
    ]
}
