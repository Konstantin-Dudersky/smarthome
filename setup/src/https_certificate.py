"""Создание сертификата HTTPS."""

import logging
import os
import shutil
from typing import Callable

CERTS_DIR: str = "~/certs"
ROOT_DIR: str = "{certs_dir}/root".format(certs_dir=CERTS_DIR)
DOMAIN_DIR: str = "{certs_dir}/{domain}"

SUBJ: str = (
    '-subj "/C={country}/ST={state}"/L={loc}/O={org}/OU={org_unit}'
    + "/CN={common_name}/emailAddress={email}"
)

ROOT_KEY: str = "openssl genrsa -des3 -out {root_dir}/{machine}.key 2048"
ROOT_PEM: str = (
    "openssl req -x509 -new -nodes -key {root_dir}/{machine}.key -sha256 "
    + "-days 1825 -out {root_dir}/{machine}.pem {subj}"
)

DOMAIN_KEY: str = "openssl genrsa -out {domain_dir}/{domain}.key 2048"
DOMAIN_CSR: str = (
    "openssl req -new -key {domain_dir}/{domain}.key "
    + "-out {domain_dir}/{domain}.csr {subj}"
)
DOMAIN_EXT: str = """
authorityKeyIdentifier=keyid,issuer
basicConstraints=CA:FALSE
keyUsage = digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment
subjectAltName = @alt_names
[alt_names]
DNS.1 = {domain}
"""
DOMAIN_CRT: str = (
    "openssl x509 -req -in {domain_dir}/{domain}.csr "
    + "-CA {root_dir}/{machine}.pem "
    + "-CAkey {root_dir}/{machine}.key "
    + "-CAcreateserial -out {domain_dir}/{domain}.crt -days 825 -sha256 "
    + "-extfile {domain_dir}/{domain}.ext"
)


def create_root(machine: str, domain: str) -> bool:
    """Создание корневого сертификата для OS.

    :param machine: имя компьютера, для которого генерируется сертификат
    :param domain: название домена, для которого будет создан сертификат
    :return: True - корневой сертификат создан
    """
    logging.info("Создаем корневой сертификат сервера в папке %s", ROOT_DIR)
    subj: str = SUBJ.format(
        country="BY",
        state="Minsk",
        loc="Minsk",
        org="Inosat",
        org_unit="Inosat",
        common_name=domain,
        email="info@i-a.by",
    )
    root_dir: str = os.path.expanduser(ROOT_DIR)
    if os.path.exists(root_dir):
        shutil.rmtree(root_dir)
    os.makedirs(root_dir)
    os.chdir(root_dir)
    os.system(ROOT_KEY.format(root_dir=root_dir, machine=machine))
    os.system(ROOT_PEM.format(root_dir=root_dir, machine=machine, subj=subj))
    logging.info("Корневой сертификат создан")
    logging.warning("Можно установить файл *.pem на клиентских машинах.")
    return True


def create_domain_server(machine: str, domain: str) -> bool:
    """Создание сертификата для домена.

    :param machine: имя компьютера, для которого генерируется сертификат
    :param domain: название домена, для которого будет создан сертификат
    :return: True - сертификат для домена создан
    """
    logging.info("Создаем сертификат для домена {domain}".format(domain=domain))
    subj: str = SUBJ.format(
        country="BY",
        state="Minsk",
        loc="Minsk",
        org="Inosat",
        org_unit="Inosat",
        common_name=domain,
        email="info@i-a.by",
    )
    os.chdir(os.path.expanduser(CERTS_DIR))
    root_dir: str = os.path.expanduser(ROOT_DIR)
    domain_dir: str = os.path.expanduser(
        DOMAIN_DIR.format(
            certs_dir=CERTS_DIR,
            domain=domain,
        ),
    )
    if os.path.exists(domain_dir):
        shutil.rmtree(domain_dir)
    os.makedirs(domain_dir)
    os.system(
        DOMAIN_KEY.format(
            domain=domain,
            domain_dir=domain_dir,
        ),
    )
    os.system(
        DOMAIN_CSR.format(
            domain=domain,
            domain_dir=domain_dir,
            subj=subj,
        ),
    )
    with open(
        "{domain_dir}/{domain}.ext".format(
            domain_dir=domain_dir,
            domain=domain,
        ),
        "w",
    ) as csr_file:
        csr_file.write(DOMAIN_EXT.format(domain=domain))
    os.system(
        DOMAIN_CRT.format(
            root_dir=root_dir,
            machine=machine,
            domain_dir=domain_dir,
            domain=domain,
        ),
    )
    return True


def create(machine: str, domain: str) -> Callable[[], None]:
    """Создать сертификат HTTPS.

    :param machine: имя компьютера, для которого генерируется сертификат
    :param domain: название домена, для которого будет создан сертификат
    :return: задача
    """

    def _create() -> None:
        if not create_root(machine, domain):
            return
        if not create_domain_server(machine, domain):
            return

    return _create


if __name__ == "__main__":
    machine: str = "test-os"
    domain: str = "test-domain"
    create_root(machine, domain)
    create_domain_server(machine, domain)
