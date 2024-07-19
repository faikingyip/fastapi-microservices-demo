from typing import Any, Dict

from asyncpg import UniqueViolationError
from fastapi import Query
from sqlalchemy import Uuid, func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.crud import get_object, get_objects
from src.constants.transaction_statuses import TransactionStatuses
from src.db.models.db_transaction import DbTransaction
from src.errors import AppServiceError, BusinessValidationError
from src.schemas.schema_transaction import SchemaTransactionCreate


async def create_transaction(
    db: AsyncSession,
    user_id,
    request: SchemaTransactionCreate,
):

    query = (
        select(func.max(DbTransaction.version).label("max_version"))
        .where(DbTransaction.user_id == user_id)
        .group_by(DbTransaction.user_id)
    )

    result = await db.execute(query)

    max_version = result.scalar_one_or_none()

    if not max_version:
        max_version = 0

    if request.amount == 0:
        bv = BusinessValidationError()
        bv.add_error(
            "amount_zero",
            "Amount cannot be 0",
            None,
        )
        raise bv

    new_record = DbTransaction(
        user_id=user_id,
        version=max_version + 1,
        amount=request.amount,
        status=TransactionStatuses.PENDING.value,
    )

    try:
        db.add(new_record)
        await db.commit()
        await db.refresh(new_record)
    except IntegrityError as ite:
        await db.rollback()
        cause = ite.orig.__cause__
        if isinstance(cause, UniqueViolationError) and cause.detail.startswith(
            "Key (user_id, version)"
        ):
            e = BusinessValidationError()
            e.add_error(
                "unique_email",
                (
                    ("Transaction id is already declared as last"),
                    ("transaction id for another transaction."),
                ),
                None,
            )
            raise e from ite
        raise AppServiceError(
            "Failed to create an transaction.",
            {"msg": str(ite)},
        ) from ite
    except SQLAlchemyError as sqlae:
        await db.rollback()
        raise AppServiceError(
            "Failed to create a transaction.",
            {"msg": str(sqlae)},
        ) from sqlae

    return new_record


async def get_transactions(
    db: AsyncSession,
    page_index: int,
    page_size: int,
    sort_by: str = Query(None),
) -> Dict[str, Any]:
    query = select(DbTransaction)
    return await get_objects(
        DbTransaction,
        db,
        query,
        page_index,
        page_size,
        sort_by,
    )


async def get_transaction(db: AsyncSession, user_id: Uuid, transaction_id: Uuid):
    return await get_object(
        db,
        select(DbTransaction).where(
            (DbTransaction.user_id == user_id) & (DbTransaction.id == transaction_id)
        ),
    )
