import os
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from src.auth import bootstrap
from src.auth.entrypoints.fastapi import app

# conftest is run before main.py when you run pytest.


# This env variable is auto
# removed once testing is completed.
os.environ["ENV"] = "Testing"
bootstrap.load_env()

bootstrap.bootstrap_api_ctx(
    db_man=bootstrap.build_db_man(),
    msg_pub_client=None,
)


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    yield TestClient(app.app)


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    # post_table.clear()
    # comments_table.clear()
    yield


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(
        app=app.app,
        base_url=client.base_url,
    ) as ac:
        yield ac
