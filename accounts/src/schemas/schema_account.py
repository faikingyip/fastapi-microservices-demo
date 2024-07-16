from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SchemaAccountCreate(BaseModel):
    """The payload for creating an account."""

    user_id: UUID = Field(
        example="2ca6f51b-e159-4f24-a17e-70d8245b29ee",
        description="Id of the user",
    )

    balance: Decimal = Field(
        example=12.99,
        description="Current balance",
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
                    "balance": "100",
                    "last_trans_id": "0e38df0b-0b9c-45aa-bb9f-10ab4e533f33",
                },
            ]
        }
    }


class SchemaAccountDisplay(BaseModel):
    """The response for a single account."""

    id: UUID
    user_id: UUID
    balance: Decimal
    version: int
    created_on: datetime
    last_updated_on: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )
