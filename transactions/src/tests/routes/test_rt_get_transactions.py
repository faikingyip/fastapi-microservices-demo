# Retrieve success for empty list
# Retrieve success for non-empty list
# Retrieve success for page index and full page size
# Retrieve success for last and incomplete page
# Retrieve success for page index and sort
# Retrieve failed on invalid sort type
# Retrieve limited to the user

import pytest
from fastapi import status
from httpx import AsyncClient

from src.common.crud import create_multiple
from src.db.models.db_transaction import DbTransaction

LIST_URL = "/api/transactions/"


@pytest.fixture
async def create_transactions(db_session):
    """Provides a method to create multiple transactions"""

    async def _create_transactions(transactions_data):
        return await create_multiple(
            DbTransaction,
            transactions_data,
            db_session,
        )

    return _create_transactions
