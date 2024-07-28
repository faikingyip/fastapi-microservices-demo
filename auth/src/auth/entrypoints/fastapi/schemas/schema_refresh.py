from pydantic import BaseModel, Field


class SchemaRefresh(BaseModel):

    refresh: str = Field(
        description="Refresh token",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "refresh": "string",
                },
            ]
        }
    }
