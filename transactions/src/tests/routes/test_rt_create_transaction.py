# Create fail for unauthenticated user.
# Create fail for expired access token user.
# Create success for authenticated user.
# Create fail on missing user_id.
# Create fail on missing amount.
# Create fail on zero amount.
# Create fail on missing last_trans_id.

import random
import string
from uuid import uuid4

import pytest
from fastapi import status
from httpx import AsyncClient

from src.common import oauth2
from src.common.crud import create_multiple
from src.db.models.db_transaction import DbTransaction

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
            "user_id": str(uuid4()),
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
