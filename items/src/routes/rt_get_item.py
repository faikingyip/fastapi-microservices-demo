from fastapi import APIRouter, Depends, Path, Response, status
from sqlalchemy import Uuid
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
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
    id: Uuid = Path(
        default=..., description="The id of the user"
    ),  # ... elipses indicates the parameter is required.
    db: AsyncSession = Depends(get_db),
    # current_user=Depends(oauth2.get_user_from_access_token),
):
    """Gets the item with the specified id."""
    # item = await ops_item.get_user_by_id(db, id)
    # if not item:
    #     response.status_code = status.HTTP_404_NOT_FOUND
    #     raise create_item_not_found_exception()
    # return item
    pass
