# Retrieve success
# Retrieve fail not found


from uuid import uuid4

import pytest
from fastapi import status
from httpx import AsyncClient

from src.common.crud import create_multiple
from src.db.models.db_item import DbItem

LIST_URL = "/api/items/"


def detail_url(item_id):
    return f"/api/items/{item_id}"


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


@pytest.mark.anyio
async def test_retrieve_success(
    async_client: AsyncClient,
    create_items,
):
    """Retrieve success"""

    items_data = [
        {"title": "Item 1", "description": "Description 1", "price": 12.99},
        {"title": "Item 2", "description": "Description 2", "price": 13.99},
        {"title": "Item 3", "description": "Description 3", "price": 14.99},
    ]
    await create_items(items_data)
    res = await async_client.get(LIST_URL)
    item2_id = res.json()["items"][1]["id"]
    res = await async_client.get(detail_url(item2_id))
    assert res.status_code == status.HTTP_200_OK
    assert res.json()["id"] == item2_id
    assert res.json()["title"] == "Item 2"
    assert res.json()["description"] == "Description 2"
    assert res.json()["price"] == "13.99"


@pytest.mark.anyio
async def test_retrieve_fail_not_found(
    async_client: AsyncClient,
    create_items,
):
    """Retrieve fail not found"""
    items_data = [
        {"title": "Item 1", "description": "Description 1", "price": 12.99},
        {"title": "Item 2", "description": "Description 2", "price": 13.99},
        {"title": "Item 3", "description": "Description 3", "price": 14.99},
    ]
    await create_items(items_data)
    res = await async_client.get(LIST_URL)
    assert len(res.json()["items"]) == 3
    res = await async_client.get(detail_url(uuid4()))
    assert res.status_code == status.HTTP_404_NOT_FOUND
