# Retrieve success for empty list
# Retrieve success for non-empty list
# Retrieve success for page index and size
# Retrieve success for page index and sort

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.orm import Session

from src.app import db_manager
from src.db.database import Base
from src.db.models.db_item import DbItem


async def create_db_tables():
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_db_tables():
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session", autouse=True)
async def setup_and_teardown_db():
    await create_db_tables()
    yield
    await drop_db_tables()


@pytest.fixture(scope="function")
async def db_session() -> Session:
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


@pytest.fixture
async def create_items(db_session):
    async def _create_items(items_data):
        items = [DbItem(**item_data) for item_data in items_data]
        db_session.add_all(items)
        await db_session.commit()
        return items

    return _create_items


@pytest.mark.anyio
async def test_retrieve_success_for_empty_list(async_client: AsyncClient):
    """Retrieve success for empty list"""

    res = await async_client.get("/api/items/")
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

    res = await async_client.get("/api/items/")
    assert res.status_code == status.HTTP_200_OK
    assert "items" in res.json()
    assert isinstance(res.json()["items"], list)
    assert len(res.json()["items"]) == 2
    assert res.json()["page_index"] == 0
    assert res.json()["page_size"] == 10
    assert res.json()["total_items"] == 2
    assert res.json()["items_in_page"] == 2


# @pytest.mark.anyio
# async def test_retrieve_success_for_page_index_and_size(async_client: AsyncClient):
#     """Retrieve success for page index and size"""

#     res = await async_client.get(
#         "/api/items/", params={"page_index": 1, "page_size": 5}
#     )
#     assert res.status_code == status.HTTP_200_OK
#     assert "items" in res.json()
#     assert len(res.json()["items"]) <= 5


# @pytest.mark.anyio
# async def test_retrieve_success_for_page_index_and_sort(async_client: AsyncClient):
#     """Retrieve success for page index and sort"""

#     res = await async_client.get(
#         "/api/items/", params={"page_index": 1, "page_size": 5, "sort_type": "title"}
#     )

#     assert res.status_code == status.HTTP_200_OK
#     assert "items" in res.json()
#     items = res.json()["items"]
#     assert all(
#         items[i]["title"] <= items[i + 1]["title"] for i in range(len(items) - 1)
#     )
