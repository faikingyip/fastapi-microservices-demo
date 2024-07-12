from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SchemaTransactionCreate(BaseModel):
    """The payload for creating a transaction."""

    user_id: UUID = Field(
        example="2ca6f51b-e159-4f24-a17e-70d8245b29ee",
        description="Id of the user",
    )

    amount: Decimal = Field(
        example=12.99,
        description="Amount",
        ge=0.01,
        decimal_places=2,
    )

    last_trans_id: UUID = Field(
        example="0e38df0b-0b9c-45aa-bb9f-10ab4e533f33",
        description="Id of the last transaction",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "user_id": "2ca6f51b-e159-4f24-a17e-70d8245b29ee",
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
    last_trans_id: UUID
    created_on: datetime
    last_updated_on: datetime

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
