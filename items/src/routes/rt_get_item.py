from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.common.database import get_db
from src.ops import ops_item
from src.schemas.schema_item import SchemaItemDisplay

router = APIRouter(prefix="/api/items", tags=["items"])


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    summary="Get by id",
    response_description="Get by id.",
    response_model=SchemaItemDisplay,
)
async def get_item(
    response: Response,
    id: UUID = Path(
        default=..., description="The id of the item"
    ),  # ... elipses indicates the parameter is required.
    db: AsyncSession = Depends(get_db),
    # current_user=Depends(oauth2.get_user_from_access_token),
):
    """Gets the item with the specified id."""
    item = await ops_item.get_item(db, id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found",
        )
    return item
