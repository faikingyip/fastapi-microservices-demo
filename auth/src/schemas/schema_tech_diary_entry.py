from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class SchemaTechDiaryEntryCreate(BaseModel):

    ref_date: datetime = Field(description="Ref Date")
    title: str = Field(description="Title", min_length=1, max_length=300)
    content: str = Field(description="Content", min_length=1, max_length=5000)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "ref_date": "2024-05-01T12:00:00+03:00",
                    "title": "title",
                    "content": "content",
                }
            ]
        }
    }


class SchemaTechDiaryEntryDisplay(BaseModel):
    id: UUID
    ref_date: datetime
    title: str
    content: str
    created_on: datetime
    last_updated_on: datetime

    class Config:
        orm_mode = True  # sqlalchemy will auto fit the data to this model.
