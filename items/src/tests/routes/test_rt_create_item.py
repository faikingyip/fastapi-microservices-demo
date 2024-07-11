# Create fail for unauthenticated user.
# Create success for authenticated user.
# Create fail on missing title.
# Create fail on empty title.
# Create fail on title too long.
# Create fail on missing description.
# Create fail on empty description.
# Create fail on description too long.
# Create fail on missing price.
# Create fail on negative price.

import random
import string

import pytest
from fastapi import status
from httpx import AsyncClient

from src.common.crud import create_multiple
from src.db.models.db_item import DbItem

LIST_URL = "/api/items/"


@pytest.fixture
async def create_items(db_session):
    """Provides a method to create multiple ite"""

    async def _create_items(items_data):
        return await create_multiple(
            DbItem,
            items_data,
            db_session,
        )

    return _create_items


@pytest.fixture
async def random_max_length_title():
    """Provides a random title of max length allowed."""

    return (
        "".join(
            random.choices(
                string.ascii_letters,
                k=254,
            )
        ),
    )


@pytest.fixture
async def random_max_length_desc():
    """Provides a random description of max length allowed."""

    return (
        "".join(
            random.choices(
                string.ascii_letters,
                k=511,
            )
        ),
    )


@pytest.mark.anyio
async def test_create_fail_for_unauthenticated_user(
    async_client: AsyncClient,
):
    """Create fail for unauthenticated user."""

    payload = {
        "title": "Item A",
        "description": "Item A description",
        "price": 12.99,
    }
    res = await async_client.post(LIST_URL, payload)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_create_success_for_authenticated_user(
    async_client: AsyncClient,
    random_max_length_title,
    random_max_length_desc,
):
    """Create success for authenticated user."""

    payload = {
        "title": random_max_length_title,
        "description": random_max_length_desc,
        "price": 12.99,
    }
    res = await async_client.post(LIST_URL, payload)
    assert res.status_code == status.HTTP_201_CREATED
    assert res.json()["id"]
    assert res.json()["created_on"]
    assert res.json()["last_updated_on"]

    res = await async_client.get(LIST_URL)
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()["items"]) == 1
    assert res.json()["items"][0]["title"] == random_max_length_title
    assert res.json()["items"][0]["description"] == random_max_length_desc


@pytest.mark.anyio
async def test_create_fail_on_missing_title(
    async_client: AsyncClient,
    random_max_length_desc,
):
    """Create fail on missing title."""

    payload = {
        "description": random_max_length_desc,
        "price": 12.99,
    }

    res = await async_client.post(LIST_URL, payload)
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_create_fail_on_empty_title(
    async_client: AsyncClient,
    random_max_length_desc,
):
    """Create fail on empty title."""

    payload = {
        "title": "",
        "description": random_max_length_desc,
        "price": 12.99,
    }

    res = await async_client.post(LIST_URL, payload)
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_create_fail_on_title_too_long(
    async_client: AsyncClient,
    random_max_length_title,
    random_max_length_desc,
):
    """Create fail on title too long."""

    payload = {
        "title": random_max_length_title + "a",
        "description": random_max_length_desc,
        "price": 12.99,
    }

    res = await async_client.post(LIST_URL, payload)
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_create_fail_on_missing_description(
    async_client: AsyncClient,
    random_max_length_title,
):
    """Create fail on missing description."""

    payload = {
        "title": random_max_length_title,
        "price": 12.99,
    }

    res = await async_client.post(LIST_URL, payload)
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_create_fail_on_empty_description(
    async_client: AsyncClient,
    random_max_length_title,
):
    """Create fail on empty description."""

    payload = {
        "title": random_max_length_title,
        "description": "",
        "price": 12.99,
    }

    res = await async_client.post(LIST_URL, payload)
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_create_fail_on_description_too_long(
    async_client: AsyncClient,
    random_max_length_title,
    random_max_length_desc,
):
    """Create fail on description too long."""

    payload = {
        "title": random_max_length_title,
        "description": random_max_length_desc + "a",
        "price": 12.99,
    }

    res = await async_client.post(LIST_URL, payload)
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_create_fail_on_missing_price(
    async_client: AsyncClient,
    random_max_length_title,
    random_max_length_desc,
):
    """Create fail on missing price."""

    payload = {
        "title": random_max_length_title,
        "description": random_max_length_desc,
    }

    res = await async_client.post(LIST_URL, payload)
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_create_fail_on_negative_price(
    async_client: AsyncClient,
    random_max_length_title,
    random_max_length_desc,
):
    """Create fail on negative price."""

    payload = {
        "title": random_max_length_title,
        "description": random_max_length_desc,
        "price": -1,
    }

    res = await async_client.post(LIST_URL, payload)
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
