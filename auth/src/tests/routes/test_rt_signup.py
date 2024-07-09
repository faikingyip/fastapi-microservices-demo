# Validation error on email address not provided.
# Validation error on invalid email address format.
# Validation error on email address too long.
# Validation error on password not provided.
# Validation error on password too long.
# Validation error on email address already in use.
# Internal server error on system errors, i.e. database connection.
# Password is encrypted.


import pytest
import pytest_asyncio
from fastapi import status
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from src.db.database import Base, get_db
from src.main import app

# DATABASE_URL = "sqlite+aiosqlite:///:memory:"
# DATABASE_URL = "sqlite+aiosqlite:///./test.db"

db_host = "localhost"
db_port = "5432"
db_name = "auth_srv_test12345"
db_user = "msdemouser"
db_pass = "msdemouser"
DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"


# Create a database engine
# engine = create_async_engine(DATABASE_URL)
engine = create_async_engine(DATABASE_URL, future=True, echo=True)

# Declare a sessionmaker with autocommit and autoflush settings
TestingSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def override_get_db():
    async with TestingSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()


app.dependency_overrides[get_db] = override_get_db


async def setup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def teardown():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


# @pytest.fixture(scope="function", autouse=True)
# async def setup_and_teardown():
#     await setup()
#     yield
#     await teardown()


client = TestClient(app)


@pytest.mark.asyncio
# @pytest.mark.usefixtures("setup_and_teardown")
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
        pass
        await teardown()
