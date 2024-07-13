# Create fail for unauthenticated user.
# Create fail for expired access token user.
# Create success for authenticated user.
# Create success for negative amount (withdraw).
# Create fail on missing amount.
# Create fail on zero amount.
# Create fail on missing last_trans_id.
# Create fail on empty last_trans_id.
# Create fail on duplicate transaction id.

import random
import string
from uuid import uuid4

import pytest
from fastapi import status
from httpx import AsyncClient

from src.common import oauth2
from src.common.crud import create_multiple
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

    email = "user@example.com"
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
        # "user_id": "0e38df0b-0b9c-45aa-bb9f-10ab4e533f33",
        "last_trans_id": "2ca6f51b-e159-4f24-a17e-70d8245b29ee",
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
        # "user_id": "0e38df0b-0b9c-45aa-bb9f-10ab4e533f33",
        "amount": 12.99,
        "last_trans_id": "2ca6f51b-e159-4f24-a17e-70d8245b29ee",
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

    last_trans_id = "2ca6f51b-e159-4f24-a17e-70d8245b29ee"
    payload = {
        # "user_id": user_id,
        "amount": 12.99,
        "last_trans_id": last_trans_id,
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
    assert res.json()["items"][0]["last_trans_id"] == last_trans_id


@pytest.mark.anyio
async def test_create_success_for_negative_amount(
    async_client: AsyncClient,
    auth_headers,
):
    """Create success for negative amount (withdraw)."""

    last_trans_id = "2ca6f51b-e159-4f24-a17e-70d8245b29ee"
    payload = {
        # "user_id": user_id,
        "amount": -50,
        "last_trans_id": last_trans_id,
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
    assert res.json()["items"][0]["last_trans_id"] == last_trans_id


@pytest.mark.anyio
async def test_create_fail_on_missing_amount(
    async_client: AsyncClient,
    auth_headers,
):
    """Create fail on missing amount."""

    payload = {
        # "user_id": "0e38df0b-0b9c-45aa-bb9f-10ab4e533f33",
        "last_trans_id": "2ca6f51b-e159-4f24-a17e-70d8245b29ee",
    }

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
    """Create fail on zero user_id."""

    payload = {
        # "user_id": "0e38df0b-0b9c-45aa-bb9f-10ab4e533f33",
        "amount": 0,
        "last_trans_id": "2ca6f51b-e159-4f24-a17e-70d8245b29ee",
    }

    with pytest.raises(BusinessValidationError):
        await async_client.post(
            LIST_URL,
            json=payload,
            headers=auth_headers,
        )


@pytest.mark.anyio
async def test_create_fail_on_missing_last_trans_id(
    async_client: AsyncClient,
    auth_headers,
):
    """Create fail on missing last_trans_id."""

    payload = {
        # "user_id": "0e38df0b-0b9c-45aa-bb9f-10ab4e533f33",
        "amount": 12.99,
    }

    res = await async_client.post(
        LIST_URL,
        json=payload,
        headers=auth_headers,
    )

    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_create_fail_on_empty_last_trans_id(
    async_client: AsyncClient,
    auth_headers,
):
    """Create fail on empty last_trans_id."""

    payload = {
        # "user_id": "0e38df0b-0b9c-45aa-bb9f-10ab4e533f33",
        "amount": 12.99,
        "last_trans_id": None,
    }

    res = await async_client.post(
        LIST_URL,
        json=payload,
        headers=auth_headers,
    )

    assert res.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.anyio
async def test_create_fail_on_duplicate_transaction_id(
    async_client: AsyncClient,
    auth_headers,
):
    """Create success for authenticated user."""

    last_trans_id = "2ca6f51b-e159-4f24-a17e-70d8245b29ee"
    payload = {
        # "user_id": str(uuid4()),
        "amount": 12.99,
        "last_trans_id": last_trans_id,
    }

    await async_client.post(
        LIST_URL,
        json=payload,
        headers=auth_headers,
    )

    with pytest.raises(BusinessValidationError):
        await async_client.post(
            LIST_URL,
            json=payload,
            headers=auth_headers,
        )
