from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status

from src.accounts.entrypoints import schemas
from src.accounts.srv_layer import services
from src.accounts.srv_layer.uow import SqlAlchemyUoW
from src.common import oauth2
from src.common.ctx.api_context import ApiContext

router = APIRouter(prefix="/api/accounts", tags=["accounts"])


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Get account for the authenticated user.",
    response_description="Get account for the authenticated user.",
    response_model=schemas.SchemaAccountDisplay,
)
async def get_account(
    # response: Response,
    api_ctx: ApiContext = Depends(
        ApiContext.get_instance_async,
    ),
    current_user=Depends(
        oauth2.get_user_from_access_token,
    ),
):
    """Gets the account with the specified id."""

    account = await services.get_by_user(
        str(current_user["id"]),
        SqlAlchemyUoW(
            api_ctx.db_man.session_local,
        ),
    )

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found",
        )

    return account


@router.get(
    "/test",
    status_code=status.HTTP_200_OK,
    summary="Get account for the authenticated user.",
    response_description="Get account for the authenticated user.",
    response_model=schemas.SchemaAccountDisplay,
)
async def test(
    # response: Response,
    # db: AsyncSession = Depends(ApiContext.get_instance().db_man.get_session),
):
    account = await services.create_account(
        str(uuid4()), SqlAlchemyUoW(ApiContext.get_instance().db_man.session_local)
    )
    return account
