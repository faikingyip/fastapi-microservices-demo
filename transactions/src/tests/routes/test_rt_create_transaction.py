# Create fail for unauthenticated user.
# Create fail for expired access token user.
# Create success for authenticated user.
# Create success for negative amount (withdraw).
# Create fail on missing amount.
# Create fail on zero amount.
# Create multiple increments version number.
# Create version number starts again for new user.

import random
import string
from uuid import uuid4

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy import select

from src.common import oauth2
from src.common.crud import create_multiple
from src.common.database import get_db
from src.db.models.db_transaction import DbTransaction
from src.errors import BusinessValidationError

LIST_URL = "/api/transactions/"


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


DEFAULT_USER_ID = "c5c7a225-222c-44e9-b228-3bf5b76a3fb2"


@pytest.fixture
async def access_token():
    """Provides a method to create a dummy access token"""

    email = "user1@example.com"
    return oauth2.create_access_token(
        data={
            "sub": email,
            "email": email,
            "first_name": "Fname",
            "last_name": "Lname",
            "user_id": DEFAULT_USER_ID,
        }
    )


@pytest.fixture
async def auth_headers(access_token):
    """Provides a method to create the authentication header"""

    return {"Authorization": f"Bearer {access_token}"}


@pytest.fixture
async def expired_access_token():
    """Provides a method to create multiple ite"""

    email = "user@example.com"
    return oauth2.create_access_token(
        data={
            "sub": email,
            "email": email,
            "first_name": "Fname",
            "last_name": "Lname",
            "user_id": str(uuid4()),
        },
        expire_mins=-1,
    )


@pytest.fixture
async def expired_auth_headers(expired_access_token):
    """Provides a method to create multiple ite"""

    return {"Authorization": f"Bearer {expired_access_token}"}


@pytest.fixture
async def random_max_length_title():
    """Provides a random title of max length allowed."""

    return "".join(
        random.choices(
            string.ascii_letters,
            k=254,
        )
    )


@pytest.fixture
async def random_max_length_desc():
    """Provides a random description of max length allowed."""

    return "".join(
        random.choices(
            string.ascii_letters,
            k=511,
        )
    )


@pytest.mark.anyio
async def test_create_fail_for_unauthenticated_user(
    async_client: AsyncClient,
):
    """Create fail for unauthenticated user."""

    payload = {
        "amount": 12.99,
    }

    res = await async_client.post(LIST_URL, json=payload)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_create_fail_for_expired_access_token_user(
    async_client: AsyncClient,
    expired_auth_headers,
):
    """Create fail for expired access token user."""

    payload = {
        "amount": 12.99,
    }

    res = await async_client.post(
        LIST_URL,
        json=payload,
        headers=expired_auth_headers,
    )

    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.anyio
async def test_create_success_for_authenticated_user(
    async_client: AsyncClient,
    auth_headers,
):
    """Create success for authenticated user."""

    payload = {
        "amount": 12.99,
    }

    res = await async_client.post(
        LIST_URL,
        json=payload,
        headers=auth_headers,
    )
    assert res.status_code == status.HTTP_201_CREATED
    assert res.json()["id"]
    assert res.json()["created_on"]
    assert res.json()["last_updated_on"]

    res = await async_client.get(LIST_URL)
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()["items"]) == 1
    assert res.json()["items"][0]["user_id"] == DEFAULT_USER_ID
    assert res.json()["items"][0]["amount"] == "12.99"
    assert res.json()["items"][0]["version"] == 1


@pytest.mark.anyio
async def test_create_success_for_negative_amount(
    async_client: AsyncClient,
    auth_headers,
):
    """Create success for negative amount (withdraw)."""

    payload = {
        "amount": -50,
    }

    res = await async_client.post(
        LIST_URL,
        json=payload,
        headers=auth_headers,
    )

    assert res.status_code == status.HTTP_201_CREATED
    assert res.json()["id"]
    assert res.json()["created_on"]
    assert res.json()["last_updated_on"]

    res = await async_client.get(LIST_URL)
    assert res.status_code == status.HTTP_200_OK
    assert len(res.json()["items"]) == 1
    assert res.json()["items"][0]["user_id"] == DEFAULT_USER_ID
    assert res.json()["items"][0]["amount"] == "-50.00"


@pytest.mark.anyio
async def test_create_fail_on_missing_amount(
    async_client: AsyncClient,
    auth_headers,
):
    """Create fail on missing amount."""

    payload = {}

    res = await async_client.post(
        LIST_URL,
        json=payload,
        headers=auth_headers,
    )

    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_create_fail_on_zero_amount(
    async_client: AsyncClient,
    auth_headers,
):
    """Create fail on zero amount."""

    payload = {
        "amount": 0,
    }

    with pytest.raises(BusinessValidationError):
        await async_client.post(
            LIST_URL,
            json=payload,
            headers=auth_headers,
        )


@pytest.mark.anyio
async def test_multiple_increments_version_number(
    async_client: AsyncClient,
    access_token,
    auth_headers,
):
    """Create multiple increments version number."""

    await async_client.post(
        LIST_URL,
        json={"amount": 12.99},
        headers=auth_headers,
    )

    await async_client.post(
        LIST_URL,
        json={"amount": 13.99},
        headers=auth_headers,
    )

    await async_client.post(
        LIST_URL,
        json={"amount": 14.99},
        headers=auth_headers,
    )

    current_user = await oauth2.get_user_from_access_token(access_token)

    async for db in get_db():
        query = (
            select(DbTransaction)
            .where(DbTransaction.user_id == current_user["id"])
            .order_by("version")
        )
        results = await db.execute(query)
        transactions = results.scalars().all()

        assert len(transactions) == 3
        assert transactions[0].version == 1 and str(transactions[0].amount) == "12.99"
        assert transactions[1].version == 2 and str(transactions[1].amount) == "13.99"
        assert transactions[2].version == 3 and str(transactions[2].amount) == "14.99"


@pytest.mark.anyio
async def test_create_version_number_starts_again_for_new_user(
    async_client: AsyncClient,
    access_token,
    auth_headers,
):
    """Create version number starts again for new user."""

    await async_client.post(
        LIST_URL,
        json={"amount": 12.99},
        headers=auth_headers,
    )

    await async_client.post(
        LIST_URL,
        json={"amount": 13.99},
        headers=auth_headers,
    )

    await async_client.post(
        LIST_URL,
        json={"amount": 14.99},
        headers=auth_headers,
    )

    current_user = await oauth2.get_user_from_access_token(access_token)

    another_email = "user2@example.com"
    another_user_id = str(uuid4())
    another_access_token = oauth2.create_access_token(
        data={
            "sub": another_email,
            "email": another_email,
            "first_name": "Fname2",
            "last_name": "Lname2",
            "user_id": another_user_id,
        }
    )
    another_auth_headers = {"Authorization": f"Bearer {another_access_token}"}
    await async_client.post(
        LIST_URL,
        json={"amount": 15.99},
        headers=another_auth_headers,
    )

    await async_client.post(
        LIST_URL,
        json={"amount": 16.99},
        headers=another_auth_headers,
    )

    await async_client.post(
        LIST_URL,
        json={"amount": 17.99},
        headers=another_auth_headers,
    )

    async for db in get_db():
        query = select(DbTransaction).order_by("created_on", "version")
        results = await db.execute(query)
        trans = results.scalars().all()

        assert len(trans) == 6
        assert (
            trans[0].version == 1
            and str(trans[0].amount) == "12.99"
            and str(trans[0].user_id) == current_user["id"]
        )
        assert (
            trans[1].version == 2
            and str(trans[1].amount) == "13.99"
            and str(trans[1].user_id) == current_user["id"]
        )
        assert (
            trans[2].version == 3
            and str(trans[2].amount) == "14.99"
            and str(trans[2].user_id) == current_user["id"]
        )

        assert (
            trans[3].version == 1
            and str(trans[3].amount) == "15.99"
            and str(trans[3].user_id) == another_user_id
        )
        assert (
            trans[4].version == 2
            and str(trans[4].amount) == "16.99"
            and str(trans[4].user_id) == another_user_id
        )
        assert (
            trans[5].version == 3
            and str(trans[5].amount) == "17.99"
            and str(trans[5].user_id) == another_user_id
        )
