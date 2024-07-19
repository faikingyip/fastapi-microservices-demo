from enum import Enum
from typing import Optional

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.database import get_db
from src.ops import ops_transaction
from src.schemas.schema_transaction import SchemaTransactionsDisplay

router = APIRouter(prefix="/api/transactions", tags=["transactions"])


class TransactionDisplaySortTypes(str, Enum):
    """Defines the available sort types that can be used."""

    Created_on = "created_on"


transaction_sort_type_map = {
    TransactionDisplaySortTypes.Created_on: "created_on desc",
}


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Get the list of transactions.",
    response_description="The list of available transactions",
    response_model=SchemaTransactionsDisplay,
)
async def get_transactions(
    response: Response,
    page_index: Optional[int] = Query(
        description="0 based index reference to a page",
        default=0,
        ge=0,
    ),
    page_size: Optional[int] = Query(
        description="How many transactions per page",
        default=10,
        ge=1,
        le=100,
    ),
    sort_type: TransactionDisplaySortTypes = TransactionDisplaySortTypes.Created_on,
    db: AsyncSession = Depends(get_db),
):

    sort_by = (
        transaction_sort_type_map[sort_type]
        if sort_type
        else transaction_sort_type_map[TransactionDisplaySortTypes.Created_on]
    )

    data = await ops_transaction.get_transactions(
        db, page_index=page_index, page_size=page_size, sort_by=sort_by
    )

    return SchemaTransactionsDisplay(**data)


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
#         raise create_transaction_not_found_exception()

#     return Response(status_code=status.HTTP_204_NO_CONTENT)
