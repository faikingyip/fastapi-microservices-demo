import json

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.common import oauth2
from src.common.database import get_db
from src.common.rabbit_mq import get_rmq
from src.event.publishers.transaction_created_publisher import (
    TransactionCreatedPublisher,
)
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
    rmq_cli=Depends(get_rmq),
    current_user=Depends(oauth2.get_user_from_access_token),
):
    tran = await ops_transaction.create_transaction(
        db,
        current_user["id"],
        request,
    )

    with rmq_cli:
        TransactionCreatedPublisher(rmq_cli).publish(
            json.dumps(
                {
                    "user_id": str(tran.user_id),
                    "version": tran.version,
                    "amount": str(tran.amount),
                    "status": tran.status,
                }
            )
        )

    return tran
