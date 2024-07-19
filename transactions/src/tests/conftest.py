import os
from typing import AsyncGenerator, Generator
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.app import app, config_db, db_manager, load_env
from src.common import oauth2
from src.common.database import Base

# conftest is run before main.py when you run pytest.


# This env variable is auto
# removed once testing is completed.
os.environ["ENV"] = "Testing"
load_env()
config_db()


@pytest.fixture(scope="session")
def anyio_backend():
    """Tells pytest that calls are all async."""
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    yield TestClient(app=app)


@pytest.fixture()
async def async_client(client) -> AsyncGenerator:
    """Creates an async client to make calls to
    the endpoints."""
    async with AsyncClient(
        app=app,
        base_url=client.base_url,
    ) as ac:
        yield ac


async def create_db_tables():
    """Creates all tables in the database"""
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db_tables():
    """Drops all tables in the database."""
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session", autouse=True)
async def setup_and_teardown_db():
    """Session scoped setup and teardown"""
    await create_db_tables()
    yield
    await drop_db_tables()


@pytest.fixture(scope="function")
async def db_session() -> AsyncSession:
    session = db_manager.SessionLocal()
    try:
        yield session
    finally:
        await session.close()


@pytest.fixture(autouse=True)
async def clear_data(db_session):
    """Reset data in all tables defined by Base"""
    for table in reversed(Base.metadata.sorted_tables):
        await db_session.execute(table.delete())
    await db_session.commit()


DEFAULT_USER_ID = "c5c7a225-222c-44e9-b228-3bf5b76a3fb2"


@pytest.fixture
async def access_token():
    """Provides a method to create a dummy access token"""

    email = "user1@example.com"
    return oauth2.create_access_token(
        data={
            "sub": email,
            "email": email,
            "first_name": "Fname",
            "last_name": "Lname",
            "user_id": DEFAULT_USER_ID,
        }
    )


@pytest.fixture
async def auth_headers(access_token):
    """Provides a method to create the authentication header"""

    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
async def expired_access_token():
    """Provides a method to create multiple ite"""

    email = "user@example.com"
    return oauth2.create_access_token(
        data={
            "sub": email,
            "email": email,
            "first_name": "Fname",
            "last_name": "Lname",
            "user_id": str(uuid4()),
        },
        expire_mins=-1,
    )


@pytest.fixture
async def expired_auth_headers(expired_access_token):
    """Provides a method to create multiple ite"""

    return {"Authorization": f"Bearer {expired_access_token}"}
