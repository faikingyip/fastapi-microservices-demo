# Retrieve success
# Retrieve fail not found


import pytest

from src.common.crud import create_multiple
from src.db.models.db_account import DbAccount

LIST_URL = "/api/accounts/"


def detail_url(account_id):
    return f"/api/accounts/{account_id}"


@pytest.fixture
async def create_accounts(db_session):
    """Provides a method to create multiple accounts"""

    async def _create_accounts(accounts_data):
        return await create_multiple(
            DbAccount,
            accounts_data,
            db_session,
        )

    return _create_accounts


# @pytest.mark.anyio
# async def test_retrieve_success(
#     async_client: AsyncClient,
#     create_accounts,
# ):
#     """Retrieve success"""

#     accounts_data = [
#         {"user_id": "Item 1", "description": "Description 1", "price": 12.99},
#         {"title": "Item 2", "description": "Description 2", "price": 13.99},
#         {"title": "Item 3", "description": "Description 3", "price": 14.99},
#     ]
#     await create_accounts(accounts_data)
#     res = await async_client.get(LIST_URL)
#     item2_id = res.json()["items"][1]["id"]
#     res = await async_client.get(detail_url(item2_id))
#     assert res.status_code == status.HTTP_200_OK
#     assert res.json()["id"] == item2_id
#     assert res.json()["title"] == "Item 2"
#     assert res.json()["description"] == "Description 2"
#     assert res.json()["price"] == "13.99"


# @pytest.mark.anyio
# async def test_retrieve_fail_not_found(
#     async_client: AsyncClient,
#     create_accounts,
# ):
#     """Retrieve fail not found"""
#     accounts_data = [
#         {"title": "Item 1", "description": "Description 1", "price": 12.99},
#         {"title": "Item 2", "description": "Description 2", "price": 13.99},
#         {"title": "Item 3", "description": "Description 3", "price": 14.99},
#     ]
#     await create_accounts(accounts_data)
#     res = await async_client.get(LIST_URL)
#     assert len(res.json()["items"]) == 3
#     res = await async_client.get(detail_url(uuid4()))
#     assert res.status_code == status.HTTP_404_NOT_FOUND
