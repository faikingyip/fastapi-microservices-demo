import uuid
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class SchemaArticleCreate(BaseModel):
    title: str = Field(description="Title", min_length=1, max_length=300)
    content: str = Field(description="Content", min_length=1, max_length=1000)
    published: bool = Field(default=False, description="Published")
    user_id: UUID = Field(default=..., description="Publisher")

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "title",
                    "content": "content",
                    "published": False,
                    "user_id": uuid.uuid4(),
                }
            ]
        }
    }


class SchemaArticleDisplay(BaseModel):
    id: UUID
    title: str
    content: str
    published: bool
    created_on: datetime
    last_updated_on: datetime
    user_id: UUID

    class Config:
        orm_mode = True  # sqlalchemy will auto fit the data to this model.
