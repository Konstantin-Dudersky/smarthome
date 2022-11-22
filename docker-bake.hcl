/*
Запустить сборку и загрузку образов:

docker buildx bake --builder builder -f docker-bake.hcl --push pi
*/

POSTGRE_VER = "14.5"
TIMESCALEDB_VER = "2.8.1"
PYTHON_VER = "3.10.8"
POETRY_VER = "1.2.2"
DECONZ_VER = "2.19.00"

REPO = "localhost:5000"

target "sh_base_image" {
    dockerfile = "shared/Dockerfile"
    args = {
        POETRY_VER = "${POETRY_VER}",
        PYTHON_VER = "${PYTHON_VER}"
    }
    platforms = [
        "linux/amd64",
        "linux/arm64"
    ]
}

target "sh_db" {
    dockerfile = "db/Dockerfile"
    tags = [ "${REPO}/smarthome/sh_db" ]
    args = {
        POSTGRE_VER = "${POSTGRE_VER}"
        TIMESCALEDB_VER = "${TIMESCALEDB_VER}"
    }
    platforms = [ 
        "linux/amd64",
        // "linux/arm64"
    ]
}

target "sh_deconz_hub" {
    dockerfile = "deconz_hub/Dockerfile"
    tags = [ "${REPO}/smarthome/sh_deconz_hub" ]
    args = {
        DECONZ_VER="${DECONZ_VER}"
    }
    platforms = [ 
        "linux/amd64",
        "linux/arm64"
    ]
}

target "sh_driver_deconz" {
    contexts = {
        sh_base_image = "target:sh_base_image"
    }
    dockerfile = "driver_deconz/Dockerfile"
    tags = [ "${REPO}/smarthome/sh_driver_deconz" ]
    platforms = [ 
        "linux/amd64",
        "linux/arm64"
    ]
}

target "sh_setup" {
    contexts = {
        sh_base_image = "target:sh_base_image"
    }
    dockerfile = "setup/Dockerfile"
    tags = [ "${REPO}/smarthome/sh_setup" ]
    platforms = [
        "linux/amd64",
        "linux/arm64"
    ]
}

group "pi" {
    targets = [
        "sh_db", 
        "sh_deconz_hub", 
        "sh_driver_deconz", 
        "sh_setup", 
    ]
}
