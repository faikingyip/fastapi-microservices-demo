# Retrieve success
# Retrieve fail not found
# Retrieve fail for unauthenticated user
# Retrieve fail account not owned by authenticated user
# Retrieve fail for expired access token user


from uuid import uuid4

import pytest
from fastapi import status
from httpx import AsyncClient

from src.common import oauth2
from src.common.crud import create_multiple
from src.common.database import get_db
from src.db.models.db_account import DbAccount
from src.ops import ops_account

LIST_URL = "/api/accounts/"

DETAIL_URL = "/api/accounts/me"

# def detail_url(account_id):
#     return f"/api/accounts/{account_id}"


@pytest.fixture
async def access_token():
    """Provides a method to create a fake access token"""
    email = "user@example.com"
    return oauth2.create_access_token(
        data={
            "sub": email,
            "email": email,
            "first_name": "Fname",
            "last_name": "Lname",
            "user_id": str(uuid4()),
        }
    )


@pytest.fixture
async def auth_headers(access_token):
    """Provides a method to create an auth header"""
    return {"Authorization": f"Bearer {access_token}"}


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


@pytest.mark.anyio
async def test_retrieve_success(
    async_client: AsyncClient,
    access_token,
    auth_headers,
    create_accounts,
):
    """Retrieve success"""

    current_user = await oauth2.get_user_from_access_token(access_token)

    accounts_data = [
        {"user_id": uuid4(), "balance": 13, "version": 1},
        {"user_id": current_user["id"], "balance": 10, "version": 1},
        {"user_id": uuid4(), "balance": 7, "version": 1},
    ]
    await create_accounts(accounts_data)

    async for db in get_db():
        account = await ops_account.get_account_by_user(
            db,
            user_id=current_user["id"],
        )

    res = await async_client.get(
        DETAIL_URL,
        headers=auth_headers,
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.json()["id"] == str(account.id)
    assert res.json()["user_id"] == str(current_user["id"])
    assert res.json()["balance"] == "10.00"
    assert res.json()["version"] == 1


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
