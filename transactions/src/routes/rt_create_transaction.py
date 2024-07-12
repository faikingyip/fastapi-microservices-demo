from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.common import oauth2
from src.common.database import get_db
from src.ops import ops_transaction
from src.schemas.schema_transaction import (
    SchemaTransactionCreate,
    SchemaTransactionDisplay,
)

router = APIRouter(prefix="/api/transactions", tags=["transactions"])


@router.post(
    "/",
    response_model=SchemaTransactionDisplay,
    status_code=status.HTTP_201_CREATED,
    summary="Create an transaction.",
)
async def create_transaction(
    request: SchemaTransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(oauth2.get_user_from_access_token),
):
    return await ops_transaction.create_transaction(db, request)
