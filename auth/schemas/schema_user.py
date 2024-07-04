from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class SchemaUserCreate(BaseModel):
    username: str = Field(description="Username", min_length=1, max_length=300)
    password: str = Field(description="Password", min_length=1, max_length=30)

    model_config = {
        "json_schema_extra": {
            "examples": [{"username": "username", "password": "passw0rd"}]
        }
    }


class SchemaUserDisplay(BaseModel):
    id: UUID
    username: str
    created_on: datetime
    last_updated_on: datetime

    class Config:
        from_attributes = True  # sqlalchemy will auto fit the data to this model.


class SchemaChangePassword(BaseModel):
    new_password: str = Field(description="Password", min_length=1, max_length=30)

    model_config = {"json_schema_extra": {"examples": [{"new_password": "passw0rd"}]}}
