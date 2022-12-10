from ipaddress import IPv4Address

from pydantic import SecretStr

from db import ConnectionString


def test_defaults() -> None:
    conn_str = ConnectionString()

    assert (
        conn_str.url
        == "__driver__://__user__:__password__@127.0.0.1:0/__database__"
    )


def test_change_init() -> None:
    conn_str = ConnectionString(
        driver="postgresql",
        user="postgres",
        password=SecretStr("postgres"),
        host=IPv4Address("127.0.0.1"),
        port=5432,
        database="database",
    )

    assert (
        conn_str.url == "postgresql://postgres:postgres@127.0.0.1:5432/database"
    )


def test_change_after_init() -> None:
    conn_str = ConnectionString()
    conn_str.driver = "postgresql"
    conn_str.user = "postgres"
    conn_str.password = SecretStr("postgres")
    conn_str.host = IPv4Address("127.0.0.1")
    conn_str.port = 5432
    conn_str.database = "database"

    assert (
        conn_str.url == "postgresql://postgres:postgres@127.0.0.1:5432/database"
    )
