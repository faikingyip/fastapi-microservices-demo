from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.errors import AppServiceError, BusinessValidationError
from src.ops import ops_user
from src.schemas.schema_user import SchemaUserCreate, SchemaUserDisplay

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post(
    "/signup",
    response_model=SchemaUserDisplay,
    status_code=status.HTTP_201_CREATED,
    summary="Register a user.",
)
async def signup(
    request: SchemaUserCreate,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await ops_user.create_user(db, request)
    except Exception as exc:
        raise AppServiceError(str(exc), {}) from exc


@router.get("/test")
def test():

    err = BusinessValidationError()
    err.add_error("email_already_in_use", "Email already in use.", "user@example.com")
    err.add_error("password_too_weak", "Password too weak.", "")
    raise err
    return {
        "access_token": "HELLO",
    }
