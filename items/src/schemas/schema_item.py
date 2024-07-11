from datetime import datetime
from decimal import Decimal
from typing import List
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from src.constants.field_lengths import FieldLengths

# from src.constants.field_lengths import FieldLengths


class SchemaItemCreate(BaseModel):
    """The payload for creating an item."""

    title: str = Field(
        example="Item title",
        description="Title of the item",
        min_length=1,
        max_length=FieldLengths.ITEM__TITLE.value,
    )

    description: str = Field(
        example="Item description",
        description="Description of the item",
        min_length=1,
        max_length=FieldLengths.ITEM__DESC.value,
    )

    price: Decimal = Field(
        example=12.99,
        description="Price of the item",
        ge=0.01,
        decimal_places=2,
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Item title",
                    "description": "Item description",
                    "price": 12.99,
                },
            ]
        }
    }


class SchemaItemDisplay(BaseModel):
    """The response for a single item."""

    id: UUID
    title: str
    description: str
    price: Decimal
    created_on: datetime
    last_updated_on: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class SchemaItemsDisplay(BaseModel):
    """The page response for a paged list of item."""

    items: List[SchemaItemDisplay]
    page_index: int
    page_size: int
    total_items: int
    items_in_page: int
