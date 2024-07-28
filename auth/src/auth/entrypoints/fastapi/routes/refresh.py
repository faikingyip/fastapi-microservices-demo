from fastapi import APIRouter

from src import oauth2
from src.auth.entrypoints.fastapi import schemas
from src.auth.srv_layer import services

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/refresh")
async def refresh(
    # response: Response,
    request: schemas.SchemaRefresh,
):
    payload = oauth2.decode_refresh_token(
        request.refresh,
    )
    email = payload.get("sub")
    first_name = payload.get("first_name")
    last_name = payload.get("last_name")
    user_id = payload.get("user_id")
    access_token = oauth2.create_access_token(
        data=services.build_token_data(
            user_id,
            email,
            first_name,
            last_name,
        )
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "email": email,
    }
