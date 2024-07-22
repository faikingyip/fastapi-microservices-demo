# Retrieve success
# Retrieve fail for unauthenticated user
# Retrieve fail not found
# Retrieve limited to the user


from uuid import uuid4

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select

from src.common.crud import create_multiple
from src.common.ctx.api_context import ApiContext
from src.constants.transaction_statuses import TransactionStatuses
from src.db.models.db_transaction import DbTransaction

LIST_URL = "/api/transactions/"


def detail_url(trans_id):
    return f"{LIST_URL}{trans_id}"


DEFAULT_USER_ID = "c5c7a225-222c-44e9-b228-3bf5b76a3fb2"


@pytest.fixture
async def create_transactions(db_session):
    """Provides a method to create multiple ite"""

    async def _create_transactions(transactions_data):
        return await create_multiple(
            DbTransaction,
            transactions_data,
            db_session,
        )

    return _create_transactions


# Retrieve fail for unauthenticated user
# Retrieve fail not found
# Retrieve limited to the user


@pytest.mark.anyio
async def test_retrieve_success(
    async_client: AsyncClient,
    auth_headers,
    create_transactions,
):
    """Retrieve success."""

    await create_transactions(
        [
            {
                "user_id": DEFAULT_USER_ID,
                "amount": 12.99,
                "version": 1,
                "status": TransactionStatuses.PENDING.value,
            }
        ]
    )

    async for db in ApiContext.get_instance().db_man.get_session():
        query = select(DbTransaction)
        transactions = (await db.execute(query)).scalars().all()
        new_id = transactions[0].id

    res = await async_client.get(
        detail_url(new_id),
        headers=auth_headers,
    )

    assert res.status_code == status.HTTP_200_OK
    assert res.json()["id"] == str(new_id)
    assert res.json()["user_id"] == DEFAULT_USER_ID
    assert res.json()["amount"] == "12.99"
    assert res.json()["version"] == 1
    assert res.json()["status"] == TransactionStatuses.PENDING.value


@pytest.mark.anyio
async def test_retrieve_fail_for_unauthenticated_user(
    async_client: AsyncClient,
    create_transactions,
):
    """Retrieve fail for unauthenticated user."""

    await create_transactions(
        [
            {
                "user_id": DEFAULT_USER_ID,
                "amount": 12.99,
                "version": 1,
                "status": TransactionStatuses.PENDING.value,
            }
        ]
    )

    async for db in ApiContext.get_instance().db_man.get_session():
        query = select(DbTransaction)
        transactions = (await db.execute(query)).scalars().all()
        new_id = transactions[0].id

    res = await async_client.get(
        detail_url(new_id),
    )

    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_retrieve_fail_not_found(
    async_client: AsyncClient,
    auth_headers,
    create_transactions,
):
    """Retrieve fail not found."""

    await create_transactions(
        [
            {
                "user_id": DEFAULT_USER_ID,
                "amount": 12.99,
                "version": 1,
                "status": TransactionStatuses.PENDING.value,
            }
        ]
    )

    res = await async_client.get(
        detail_url(uuid4()),
        headers=auth_headers,
    )

    assert res.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_retrieve_limited_to_user(
    async_client: AsyncClient,
    auth_headers,
    create_transactions,
):
    """Retrieve limited to the user."""

    another_user_id = uuid4()

    await create_transactions(
        [
            {
                "user_id": DEFAULT_USER_ID,
                "amount": 12.99,
                "version": 1,
                "status": TransactionStatuses.PENDING.value,
            },
            {
                "user_id": another_user_id,
                "amount": 13.99,
                "version": 1,
                "status": TransactionStatuses.PENDING.value,
            },
        ]
    )

    async for db in ApiContext.get_instance().db_man.get_session():
        query = select(DbTransaction).where(DbTransaction.user_id == another_user_id)
        transactions = (await db.execute(query)).scalars().all()
        another_user_transaction_id = transactions[0].id

    res = await async_client.get(
        detail_url(another_user_transaction_id),
        headers=auth_headers,
    )

    assert res.status_code == status.HTTP_404_NOT_FOUND
