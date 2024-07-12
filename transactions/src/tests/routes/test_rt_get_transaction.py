# Retrieve success
# Retrieve fail not found
# Retrieve limited to the user


from uuid import uuid4

import pytest
from fastapi import status
from httpx import AsyncClient

from src.common.crud import create_multiple
from src.db.models.db_transaction import DbTransaction

LIST_URL = "/api/transactions/"


def detail_url(transaction_id):
    return f"/api/transactions/{transaction_id}"


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
