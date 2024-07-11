# Retrieve success for empty list
# Retrieve success for non-empty list
# Retrieve success for page index and full page size
# Retrieve success for last and incomplete page
# Retrieve success for page index and sort
# Retrieve failed on invalid sort type

import pytest
from fastapi import status
from httpx import AsyncClient

from src.common.crud import create_multiple
from src.db.models.db_item import DbItem


def detail_url(item_id):
    return f"/api/items/{id}"


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
async def test_retrieve_success_for_empty_list(async_client: AsyncClient):
    """Retrieve success for empty list"""

    res = await async_client.get(LIST_URL)
    assert res.status_code == status.HTTP_200_OK
    assert "items" in res.json()
    assert isinstance(res.json()["items"], list)
    assert len(res.json()["items"]) == 0


@pytest.mark.anyio
async def test_retrieve_success_for_non_empty_list(
    async_client: AsyncClient,
    create_items,
):
    """Retrieve success for non-empty list"""

    items_data = [
        {"title": "Item 1", "description": "Description 1", "price": 12.99},
        {"title": "Item 2", "description": "Description 2", "price": 13.99},
    ]
    await create_items(items_data)

    res = await async_client.get(LIST_URL)
    assert res.status_code == status.HTTP_200_OK
    assert "items" in res.json()
    assert isinstance(res.json()["items"], list)
    assert len(res.json()["items"]) == 2
    assert res.json()["page_index"] == 0
    assert res.json()["page_size"] == 10
    assert res.json()["total_items"] == 2
    assert res.json()["items_in_page"] == 2


@pytest.mark.anyio
async def test_retrieve_success_for_first_page_index_and_full_page_size(
    async_client: AsyncClient,
    create_items,
):
    """Retrieve success for page index and full page size"""

    items_data = [
        {"title": "Item 1", "description": "Description 1", "price": 11.99},
        {"title": "Item 2", "description": "Description 2", "price": 12.99},
        {"title": "Item 3", "description": "Description 3", "price": 13.99},
        {"title": "Item 4", "description": "Description 4", "price": 14.99},
        {"title": "Item 5", "description": "Description 5", "price": 15.99},
        {"title": "Item 6", "description": "Description 6", "price": 16.99},
        {"title": "Item 7", "description": "Description 7", "price": 17.99},
    ]
    await create_items(items_data)

    res = await async_client.get(LIST_URL, params={"page_index": 0, "page_size": 5})
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()["items"]) == 5
    assert res.json()["page_index"] == 0
    assert res.json()["page_size"] == 5
    assert res.json()["total_items"] == 7
    assert res.json()["items_in_page"] == 5


@pytest.mark.anyio
async def test_retrieve_success_for_page_index_and_size(
    async_client: AsyncClient,
    create_items,
):
    """Retrieve success for last and incomplete page"""

    items_data = [
        {"title": "Item 1", "description": "Description 1", "price": 11.99},
        {"title": "Item 2", "description": "Description 2", "price": 12.99},
        {"title": "Item 3", "description": "Description 3", "price": 13.99},
        {"title": "Item 4", "description": "Description 4", "price": 14.99},
        {"title": "Item 5", "description": "Description 5", "price": 15.99},
        {"title": "Item 6", "description": "Description 6", "price": 16.99},
        {"title": "Item 7", "description": "Description 7", "price": 17.99},
    ]
    await create_items(items_data)

    res = await async_client.get(LIST_URL, params={"page_index": 1, "page_size": 5})
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()["items"]) == 2
    assert res.json()["page_index"] == 1
    assert res.json()["page_size"] == 5
    assert res.json()["total_items"] == 7
    assert res.json()["items_in_page"] == 2


@pytest.mark.anyio
async def test_retrieve_success_for_page_index_and_sort(
    async_client: AsyncClient,
    create_items,
):
    """Retrieve success for page index and sort"""

    items_data = [
        {"title": "Item 2", "description": "Description 2", "price": 11.99},
        {"title": "Item 4", "description": "Description 4", "price": 12.99},
        {"title": "Item 6", "description": "Description 6", "price": 13.99},
        {"title": "Item 1", "description": "Description 1", "price": 14.99},
        {"title": "Item 3", "description": "Description 3", "price": 15.99},
        {"title": "Item 5", "description": "Description 5", "price": 16.99},
        {"title": "Item 7", "description": "Description 7", "price": 17.99},
    ]
    await create_items(items_data)

    res = await async_client.get(
        LIST_URL,
        params={
            "page_index": 0,
            "page_size": 5,
            "sort_type": "title",
        },
    )

    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()["items"]) == 5
    assert res.json()["page_index"] == 0
    assert res.json()["page_size"] == 5
    assert res.json()["total_items"] == 7
    assert res.json()["items_in_page"] == 5
    items = res.json()["items"]
    assert all(
        items[i]["title"] <= items[i + 1]["title"] for i in range(len(items) - 1)
    )


@pytest.mark.anyio
async def test_retrieve_failed_on_invalid_sort_type(
    async_client: AsyncClient,
    create_items,
):
    """Retrieve failed on invalid sort type"""

    items_data = [
        {"title": "Item 1", "description": "Description 1", "price": 12.99},
        {"title": "Item 2", "description": "Description 2", "price": 13.99},
    ]
    await create_items(items_data)

    res = await async_client.get(
        LIST_URL,
        params={
            "page_index": 0,
            "page_size": 5,
            "sort_type": "invalid",
        },
    )
    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
