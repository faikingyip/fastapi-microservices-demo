from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field
from src.constants.field_lengths import FieldLengths


class SchemaUserCreate(BaseModel):
    email: EmailStr = Field(
        example="user@example.com",
        description="Email",
        min_length=1,
        max_length=FieldLengths.EMAIL.value,
    )
    password: str = Field(
        description="Password",
        min_length=1,
        max_length=30,
    )

    first_name: str = Field(
        description="First name",
        min_length=1,
        max_length=50,
    )

    last_name: str = Field(
        description="Last name",
        min_length=1,
        max_length=80,
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "user@example.com",
                    "password": "passw0rd",
                    "first_name": "John",
                    "last_name": "Doe",
                },
            ]
        }
    }


class SchemaUserDisplay(BaseModel):
    id: UUID
    email: str
    first_name: str
    last_name: str
    created_on: datetime
    last_updated_on: datetime

    class Config:
        # sqlalchemy will auto fit the data to this model.
        from_attributes = True


# class SchemaChangePassword(BaseModel):
#     new_password: str = Field(
#         description="Password",
#         min_length=1,
#         max_length=30,
#     )

#     model_config = {
#         "json_schema_extra": {
#             "examples": [{"new_password": "passw0rd"}],
#         },
#     }
