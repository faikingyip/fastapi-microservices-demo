from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Path, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.common import oauth2
from src.common.ctx.api_context import ApiContext
from src.ops import ops_transaction
from src.schemas.schema_transaction import SchemaTransactionDisplay

router = APIRouter(prefix="/api/transactions", tags=["transactions"])


@router.get(
    "/{id}",
    status_code=status.HTTP_200_OK,
    summary="Get by id",
    response_description="Get by id.",
    response_model=SchemaTransactionDisplay,
)
async def get_transaction(
    response: Response,
    id: UUID = Path(
        default=..., description="The id of the transaction"
    ),  # ... elipses indicates the parameter is required.
    db: AsyncSession = Depends(ApiContext.get_instance().db_man.get_session),
    current_user=Depends(oauth2.get_user_from_access_token),
):
    """Gets the transaction with the specified id."""
    transaction = await ops_transaction.get_transaction(db, current_user["id"], id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found",
        )
    return transaction
