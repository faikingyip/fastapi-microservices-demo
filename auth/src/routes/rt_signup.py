from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.database import get_db
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
    return await ops_user.create_user(db, request)


@router.get("/test")
def test():
    return {
        "access_token": "HELLO",
    }
