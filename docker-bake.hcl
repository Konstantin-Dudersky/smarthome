/*
Запустить сборку и загрузку образов:

docker buildx bake --builder builder -f docker-bake.hcl --push pi
*/

variable "POSTGRE_VER" { default = "14.5" }
variable "TIMESCALEDB_VER" { default = "2.8.1" }
variable "PYTHON_VER" { default = "3.10.8" }
variable "POETRY_VER" { default = "1.2.2" }
variable "DECONZ_VER" { default = "2.19.00" }


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
    tags = [ "konstantindudersky/sh_db" ]
    args = {
        POSTGRE_VER = "${POSTGRE_VER}"
        TIMESCALEDB_VER = "${TIMESCALEDB_VER}"
    }
    platforms = [ 
        "linux/amd64",
        "linux/arm64"
    ]
}

target "sh_deconz_hub" {
    dockerfile = "deconz_hub/Dockerfile"
    tags = [ "konstantindudersky/sh_deconz_hub" ]
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
    tags = [ "konstantindudersky/sh_driver_deconz" ]
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
    tags = [ "konstantindudersky/sh_setup" ]
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
