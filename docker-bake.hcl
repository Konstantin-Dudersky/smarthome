/*
Запустить сборку и загрузку образов:

docker buildx bake --builder builder -f docker-bake.hcl --push pi
*/

variable "POSTGRE_VER" { default = "14.5" }
variable "TIMESCALEDB_VER" { default = "2.8.1" }
variable "PYTHON_VER" { default = "3.10.8" }
variable "POETRY_VER" { default = "1.2.2" }
variable "DECONZ_VER" { default = "2.18.02" }

target "sh_base_image" {
    dockerfile = "shared/Dockerfile"
    platforms = [
        "linux/amd64",
        "linux/arm64"
    ]
}

target "sh_db" {
    dockerfile = "db/Dockerfile"
    tags = [ "konstantindudersky/sh_db" ]
    platforms = [ 
        "linux/amd64",
        "linux/arm64"
    ]
}

target "sh_deconz_hub" {
    dockerfile = "deconz_hub/Dockerfile"
    tags = [ "konstantindudersky/sh_deconz_hub" ]
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
    targets = ["sh_db", "sh_deconz_hub", "sh_setup"]
}
