from enum import Enum
from typing import Optional

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.database import get_db
from src.ops import ops_item
from src.schemas.schema_item import SchemaItemsDisplay

router = APIRouter(prefix="/api/items", tags=["items"])


class ItemDisplaySortTypes(str, Enum):
    """Defines the available sort types that can be used."""

    TITLE = "title"


item_sort_type_map = {
    ItemDisplaySortTypes.TITLE: "title, description",
}


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Get the list of items.",
    response_description="The list of available items",
    response_model=SchemaItemsDisplay,
)
async def get_items(
    response: Response,
    page_index: Optional[int] = Query(
        description="0 based index reference to a page",
        default=0,
        ge=0,
    ),
    page_size: Optional[int] = Query(
        description="How many items per page",
        default=10,
        ge=1,
        le=100,
    ),
    sort_type: ItemDisplaySortTypes = ItemDisplaySortTypes.TITLE,
    db: AsyncSession = Depends(get_db),
):
    sort_by = (
        item_sort_type_map[sort_type]
        if sort_type
        else item_sort_type_map[ItemDisplaySortTypes.TITLE]
    )

    data = await ops_item.get_items(
        db, page_index=page_index, page_size=page_size, sort_by=sort_by
    )

    return SchemaItemsDisplay(**data)


# @router.delete(
#     "/{id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete the user"
# )
# async def delete_user(
#     response: Response,
#     id: UUID = Path(default=..., description="The id of the user"),
#     db: AsyncSession = Depends(get_db),
#     current_user: SchemaUserDisplay = Depends(oauth2.get_current_user),
# ):
#     # """
#     # Gets the user with the specified id.

#     # - **id** The user id
#     # """
#     count = await ops_user.delete_user(db, id)
#     if count == 0:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         raise create_item_not_found_exception()

#     return Response(status_code=status.HTTP_204_NO_CONTENT)
