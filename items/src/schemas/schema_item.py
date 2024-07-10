from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

# from src.constants.field_lengths import FieldLengths


class SchemaItemDisplay(BaseModel):
    id: UUID
    title: str
    description: str
    price: Decimal
    created_on: datetime
    last_updated_on: datetime

    class Config:
        # sqlalchemy will auto fit the data to this model.
        from_attributes = True
