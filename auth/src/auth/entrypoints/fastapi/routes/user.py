from fastapi import APIRouter, Depends, status

from src.auth.entrypoints.fastapi import schemas
from src.common.ctx.api_context import ApiContext
from src.utils import oauth2

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Get the currently authenticated user.",
    response_description="Get by id.",
    response_model=schemas.SchemaUserDisplay,
)
async def get_me(
    api_ctx: ApiContext = Depends(
        ApiContext.get_instance_async,
    ),
    current_user: schemas.SchemaUserDisplay = Depends(
        oauth2.get_current_user,
    ),
):
    """Gets the currently authenticated user."""
    user = await services.get_by_email(
        (await current_user).email,
        api_ctx.uow,
    )
    return user

    # class UserDisplaySortType(str, Enum):
    #     username = "username"
    #     most_recently_created = "most_recently_created"
    #     most_recently_updated = "most_recently_updated"

    # @router.get(
    #     "/",
    #     status_code=status.HTTP_200_OK,
    #     summary="Get users",
    #     description="Get users.",
    #     response_description="The list of available blogs",
    #     response_model=List[SchemaUserDisplay],
    # )
    # async def get_users(
    #     response: Response,
    #     page_index: Optional[int] = Query(
    #         description="0 based index reference to a page", default=0, ge=0
    #     ),
    #     page_size: Optional[int] = Query(
    #         description="How many items per page", default=10, ge=1, le=100
    #     ),
    #     sort_type: UserDisplaySortType = UserDisplaySortType.most_recently_created,
    #     db: AsyncSession = Depends(get_db),
    #     current_user: SchemaUserDisplay = Depends(oauth2.get_current_user),
    # ):

    #     sort_by = "username"
    #     if sort_type == UserDisplaySortType.username:
    #         sort_by = "username"
    #     elif sort_type == UserDisplaySortType.most_recently_created:
    #         sort_by = "created_on DESC, username"
    #     elif sort_type == UserDisplaySortType.most_recently_updated:
    #         sort_by = "last_updated_on DESC, username"

    #     return await __get_users(
    #         db, page_index=page_index, page_size=page_size, sort_by=sort_by
    #     )

    # async def __get_users(
    #     db: AsyncSession,
    #     page_index: Optional[int] = Query(
    #         description="0 based index reference to a page", default=0, ge=0
    #     ),
    #     page_size: Optional[int] = Query(
    #         description="How many items per page", default=10, ge=1, le=100
    #     ),
    # sort_by: str = (
    #     Query(
    #         description='columns to sort by, i.e. "name, created_on DESC"',
    #         default=None,
    #     ),
    # )


# ):
#     return await ops_user.get_users(
#         db, page_index=page_index, page_size=page_size, sort_by=sort_by
#     )


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
#     "/{id}",
#     status_code=status.HTTP_204_NO_CONTENT,
#     summary="Delete the user"
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
