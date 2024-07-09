# from typing import AsyncGenerator, Generator  # use type hinting with out fixtures

# import pytest
# from fastapi.testclient import (
#     TestClient,
# )  # This allows us to interact with the API without having to start the fast api server.
# from httpx import AsyncClient  # We use this to actually make the request.

# from src.main import app


# # This fixture will run only once for the entire session.
# @pytest.fixture(scope="session")
# def anyio_backend():
#     # When we use an async function in fastapi we need to have an async platform to run on.
#     # So this tells fastapi to use the built-in asyncio framework to run the tests.
#     return "asyncio"


# # Can be shared between many tests.
# @pytest.fixture()
# def client() -> Generator:
#     yield TestClient(app)


# # Can be shared between many tests and autouse means it will run on every test.
# @pytest.fixture(autouse=True)
# async def db() -> AsyncGenerator:
#     yield


# @pytest.fixture()
# async def async_client(client) -> AsyncGenerator:
#     async with AsyncClient(app=app, base_url=client.base_url) as ac:
#         yield ac
