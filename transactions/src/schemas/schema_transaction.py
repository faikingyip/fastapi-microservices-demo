from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SchemaTransactionCreate(BaseModel):
    """The payload for creating a transaction."""

    amount: Decimal = Field(
        example=12.99,
        description="Amount",
        decimal_places=2,
    )

    # last_trans_id: UUID = Field(
    #     example="0e38df0b-0b9c-45aa-bb9f-10ab4e533f33",
    #     description="Id of the last transaction",
    # )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "amount": "100",
                    "last_trans_id": "0e38df0b-0b9c-45aa-bb9f-10ab4e533f33",
                },
            ]
        }
    }


class SchemaTransactionDisplay(BaseModel):
    """The response for a single transaction."""

    id: UUID
    user_id: UUID
    amount: Decimal
    created_on: datetime
    last_updated_on: datetime
    version: int
    status: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class SchemaTransactionsDisplay(BaseModel):
    """The page response for a paged list of transactions."""

    items: List[SchemaTransactionDisplay]
    page_index: int
    page_size: int
    total_items: int
    items_in_page: int
