from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src import oauth2
from src.db.database import get_db
from src.ops import ops_item
from src.schemas.schema_item import SchemaItemCreate, SchemaItemDisplay

router = APIRouter(prefix="/api/items", tags=["items"])


@router.post(
    "/",
    response_model=SchemaItemDisplay,
    status_code=status.HTTP_201_CREATED,
    summary="Create an item.",
)
async def create_item(
    request: SchemaItemCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(oauth2.get_user_from_access_token),
):
    print("AAAAAAAAAAAAAAAAAAAa")
    print(current_user)
    return await ops_item.create_item(db, request)
