from fastapi import APIRouter, HTTPException
from src import oauth2
from src.errors import UnauthorizedError
from src.schemas.schema_refresh import SchemaRefresh

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/refresh")
async def refresh(
    # response: Response,
    request: SchemaRefresh,
):
    try:
        payload = oauth2.decode_refresh_token(request.refresh)
    except UnauthorizedError as uae:
        raise HTTPException(status_code=401, detail=uae.message) from uae

    email = payload.get("sub")
    access_token = oauth2.create_access_token(data={"sub": email})
    # refresh_token = oauth2.create_refresh_token(data={"sub": email})
    return {
        "access": access_token,
        # "refresh": refresh_token,
        # "token_type": "bearer",
        "email": email,
    }
