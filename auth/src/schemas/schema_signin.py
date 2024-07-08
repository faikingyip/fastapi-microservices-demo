from pydantic import BaseModel, Field


class SchemaSignin(BaseModel):

    email: str = Field(
        description="Email to sign in",
    )
    password: str = Field(
        description="Password",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "user@example.com",
                    "password": "string",
                },
            ]
        }
    }
