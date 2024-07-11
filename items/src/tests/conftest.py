import os
from typing import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.app import app, config_db, db_manager
from src.db.database import Base

# conftest is run before main.py when you run pytest.


# This env variable is auto
# removed once testing is completed.
os.environ["ENV"] = "Testing"
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
