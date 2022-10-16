target "sh_base_image" {
    dockerfile = "shared/Dockerfile"
    tags = [
        "konstantindudersky/sh_base_image"
    ]
    platforms = [
        // "linux/amd64"
        "linux/arm64"
    ]
}

target "sh_setup" {
    contexts = {
        sh_base_image = "target:sh_base_image"
    }
    dockerfile = "setup/Dockerfile"
    tags = [
    "konstantindudersky/sh_setup"
    ]
    platforms = [
        "linux/amd64",
        "linux/arm"
    ]
}
