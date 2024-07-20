from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.common import oauth2

# from src.common.database import get_db
from src.common.ctx.api_context import ApiContext
from src.ops import ops_account
from src.schemas.schema_account import SchemaAccountDisplay

router = APIRouter(prefix="/api/accounts", tags=["accounts"])


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Get account for the authenticated user.",
    response_description="Get account for the authenticated user.",
    response_model=SchemaAccountDisplay,
)
async def get_account(
    # response: Response,
    db: AsyncSession = Depends(ApiContext.get_instance().db_man.get_session),
    current_user=Depends(oauth2.get_user_from_access_token),
):
    """Gets the account with the specified id."""

    account = await ops_account.get_account_by_user(
        db,
        current_user["id"],
    )

    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found",
        )
    return account
