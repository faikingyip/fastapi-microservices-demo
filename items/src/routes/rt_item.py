from enum import Enum
from typing import Optional

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.database import get_db
from src.ops import ops_item
from src.schemas.schema_item import SchemaItemsDisplay

router = APIRouter(prefix="/api/items", tags=["items"])


# @router.get(
#     "/me",
#     status_code=status.HTTP_200_OK,
#     summary="Get the currently authenticated user.",
#     response_description="Get by id.",
#     response_model=SchemaUserDisplay,
# )
# async def get_me(
#     response: Response,
#     db: AsyncSession = Depends(get_db),
#     current_user: SchemaUserDisplay = Depends(oauth2.get_current_user),
# ):
#     """Gets the currently authenticated user."""
#     item = await ops_item.get_user_by_id(db, (await current_user).id)
#     if not item:
#         # response.status_code = status.HTTP_404_NOT_FOUND
#         raise NotFoundError("Not found")
#     return item


# @router.get("/test")
# def test(
#     response: Response,
# ):
#     return {
#         "access_token": "HELLO",
#     }


class ItemDisplaySortType(str, Enum):
    title = "title"


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Get the list of items.",
    response_description="The list of available items",
    response_model=SchemaItemsDisplay,
    # response_model=List[SchemaItemDisplay],
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
    sort_type: ItemDisplaySortType = ItemDisplaySortType.title,
    db: AsyncSession = Depends(get_db),
):
    sort_by = "title"
    if sort_type == ItemDisplaySortType.title:
        sort_by = "title, description"

    data = await __get_items(
        db, page_index=page_index, page_size=page_size, sort_by=sort_by
    )

    return SchemaItemsDisplay(**data)


async def __get_items(
    db: AsyncSession,
    page_index: Optional[int] = Query(
        description="0 based index reference to a page", default=0, ge=0
    ),
    page_size: Optional[int] = Query(
        description="How many items per page", default=10, ge=1, le=100
    ),
    sort_by: str = Query(
        description='columns to sort by, i.e. "name, created_on DESC"', default=None
    ),
):
    return await ops_item.get_items(
        db, page_index=page_index, page_size=page_size, sort_by=sort_by
    )


# @router.get(
#     "/{id}",
#     status_code=status.HTTP_200_OK,
#     summary="Get by id",
#     response_description="Get by id.",
#     response_model=SchemaUserDisplay,
# )
# async def get_user_by_id(
#     response: Response,
#     id: UUID = Path(
#         default=..., description="The id of the user"
#     ),  # ... elipses indicates the parameter is required.
#     db: AsyncSession = Depends(get_db),
#     current_user: SchemaUserDisplay = Depends(oauth2.get_current_user),
# ):
#     # """
#     # Gets the user with the specified id.

#     # - **id** The user id
#     # """
#     item = await ops_user.get_user_by_id(db, id)
#     if not item:
#         response.status_code = status.HTTP_404_NOT_FOUND
#         raise create_item_not_found_exception()
#     return item


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
