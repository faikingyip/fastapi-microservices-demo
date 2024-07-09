# Validation error on email address not provided.
# Validation error on invalid email address format.
# Validation error on email address too long.
# Validation error on password not provided.
# Validation error on password too long.
# Validation error on email address already in use.
# Internal server error on system errors, i.e. database connection.
# Password is encrypted.


import pytest
from fastapi import status
from httpx import AsyncClient

from src.db.database import Base, db_manager
from src.main import app


async def setup():
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def teardown():
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# @pytest.fixture(scope="function", autouse=True)
# async def setup_and_teardown():
#     await setup()
#     yield
#     await teardown()


@pytest.mark.asyncio
async def test_signup_success():
    try:
        await setup()
        payload = {
            "email": "testuser@example.com",
            "password": "securepassword",
            "first_name": "Test",
            "last_name": "User",
        }
        async with AsyncClient(
            app=app, base_url="http://localhost:8000"
        ) as async_client:
            response = await async_client.post("/api/users/signup", json=payload)
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == payload["email"]
        assert data["first_name"] == payload["first_name"]
        assert data["last_name"] == payload["last_name"]
        assert "id" in data
        assert "created_on" in data
        assert "last_updated_on" in data
    finally:
        await teardown()
