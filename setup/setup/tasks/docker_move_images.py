"""Изменение тегов в образах."""

import logging
import subprocess

from ..internal.base_task import BaseTask

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class DockerMoveImages(BaseTask):
    """Переместить образы между репозиторями."""

    def __init__(
        self,
        profile: str,
        repo_from: str,
        repo_to: str,
        arch: str = "linux/amd64",
        desc: str = "Перемещение образов docker между репозиториями",
        need_confirm: bool = True,
    ) -> None:
        super().__init__(desc, need_confirm)
        self.__profile = profile
        self.__repo_from = repo_from
        self.__repo_to = repo_to
        self.__arch = arch

    def _execute(self) -> None:
        target_images = self.__get_images_from_compose(self.__profile)
        log.info("target images: \n{0}\n".format(target_images))
        images_wo_repo = self.__remove_repo(
            images=target_images,
            repo=self.__repo_to,
        )
        log.info("images w/o repo: \n{0}\n".format(images_wo_repo))
        self.__pull_images(images_wo_repo, self.__repo_from, self.__arch)
        self.__add_tag(
            images=images_wo_repo,
            repo_from=self.__repo_from,
            repo_to=self.__repo_to,
        )
        self.__push_images(images_wo_repo, self.__repo_to)

    def __get_images_from_compose(self, profile: str) -> list[str]:
        cmd: str = "docker compose --profile {profile} config --images"
        return (
            subprocess.run(
                args=cmd.format(profile=profile).split(),
                capture_output=True,
                text=True,
            )
            .stdout.strip()
            .split("\n")
        )

    def __pull_images(
        self,
        images: list[str],
        repo_from: str,
        arch: str = "linux/amd64",
    ) -> None:
        log.debug(
            "pulling images from repo: {0}, arch: {1}".format(
                repo_from,
                arch,
            ),
        )
        cmd: str = "docker pull --platform {arch} {repo_from}/{image}"
        for image in images:
            subprocess.run(
                args=cmd.format(
                    arch=arch,
                    image=image,
                    repo_from=repo_from,
                ).split(),
            )

    def __push_images(self, images: list[str], repo_to: str) -> None:
        cmd: str = "docker push {repo_to}/{image}"
        for image in images:
            subprocess.run(
                cmd.format(
                    image=image,
                    repo_to=repo_to,
                ).split(),
            )

    def __remove_repo(self, images: list[str], repo: str) -> list[str]:
        images_wo_repo: list[str] = []
        for image in images:
            if repo not in image:
                continue
            image_wo_repo = image.replace(repo + "/", "")
            images_wo_repo.append(image_wo_repo)
        return images_wo_repo

    def __add_tag(
        self,
        images: list[str],
        repo_from: str,
        repo_to: str,
    ) -> None:
        cmd: str = "docker tag {repo_from}/{image} {repo_to}/image"
        for image in images:
            subprocess.run(
                cmd.format(
                    image=image,
                    repo_from=repo_from,
                    repo_to=repo_to,
                ).split(),
            )
