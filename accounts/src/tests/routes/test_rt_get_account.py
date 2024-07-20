# Retrieve success
# Retrieve fail for unauthenticated user
# Retrieve fail account not owned by authenticated user
# Retrieve fail not found
# Retrieve fail for expired access token user


from uuid import uuid4

import pytest
from fastapi import status
from httpx import AsyncClient

from src.common import oauth2
from src.common.ctx.api_context import ApiContext
from src.common.db.crud import create_multiple

# from src.common.database import get_db
from src.db.models.db_account import DbAccount
from src.ops import ops_account

LIST_URL = "/api/accounts/"

DETAIL_URL = "/api/accounts/me"

# def detail_url(account_id):
#     return f"/api/accounts/{account_id}"


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

    async for db in ApiContext.get_instance().db_man.get_session():
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


@pytest.mark.anyio
async def test_retrieve_fai_for_unauthenticated_user(
    async_client: AsyncClient,
    create_accounts,
):
    """Retrieve fail for unauthenticated user"""

    accounts_data = [
        {"user_id": uuid4(), "balance": 13, "version": 1},
        {"user_id": uuid4(), "balance": 10, "version": 1},
        {"user_id": uuid4(), "balance": 7, "version": 1},
    ]
    await create_accounts(accounts_data)

    res = await async_client.get(
        DETAIL_URL,
    )

    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_retrieve_fail_not_owned_by_authenticated_user(
    async_client: AsyncClient,
    access_token,
    auth_headers,
    create_accounts,
):
    """Retrieve fail account not owned by authenticated user"""

    accounts_data = [
        {"user_id": uuid4(), "balance": 13, "version": 1},
    ]
    await create_accounts(accounts_data)

    res = await async_client.get(
        DETAIL_URL,
        headers=auth_headers,
    )

    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_retrieve_fail_for_expired_access_token_user(
    async_client: AsyncClient,
    expired_auth_headers,
):
    """Retrieve fail for expired access token user."""

    res = await async_client.get(
        DETAIL_URL,
        headers=expired_auth_headers,
    )

    assert res.status_code == status.HTTP_401_UNAUTHORIZED
