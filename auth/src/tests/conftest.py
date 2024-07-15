import os
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from src.app import app, config_db, load_env

# conftest is run before main.py when you run pytest.


# This env variable is auto
# removed once testing is completed.
os.environ["ENV"] = "Testing"
load_env()
config_db()


# @pytest.fixture(scope="session", autouse=True)
# async def set_test_env():
#     load_env()
#     os.environ["ENV"] = "Testing"
#     yield
#     del os.environ["ENV"]


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    # post_table.clear()
    # comments_table.clear()
    yield


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    async with AsyncClient(
        app=app,
        base_url=client.base_url,
    ) as ac:
        yield ac
