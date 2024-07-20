from asyncpg import UniqueViolationError
from fastapi import HTTPException
from sqlalchemy import Uuid, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.crud import get_object
from src.db.models.db_account import DbAccount
from src.errors import AppServiceError, BusinessValidationError


async def create_account(
    db: AsyncSession,
    user_id,
):

    new_record = DbAccount(
        user_id=user_id,
        balance=0,
        version=0,
    )

    try:
        db.add(new_record)
        await db.commit()
        await db.refresh(new_record)
    except IntegrityError as ite:
        await db.rollback()
        cause = ite.orig.__cause__
        if isinstance(cause, UniqueViolationError) and cause.detail.startswith(
            "Key (user_id)"
        ):
            e = BusinessValidationError()
            e.add_error("unique_user_id", "User already has an account.", None)
            raise e from ite
        raise AppServiceError(
            "Failed to create an account.",
            {"msg": str(ite)},
        ) from ite
    except SQLAlchemyError as sqlae:
        await db.rollback()
        raise AppServiceError(
            "Failed to create an account.",
            {"msg": str(sqlae)},
        ) from sqlae
    return new_record


async def update_account(
    db: AsyncSession,
    user_id,
    request,
):

    try:
        amount = request["amount"]
        version = request["version"]

        if amount == 0:
            e = BusinessValidationError()
            e.add_error(
                "invalid_amount",
                "The amount cannot be 0.",
                None,
            )
            raise e

        result = await db.execute(
            select(DbAccount).filter(DbAccount.user_id == user_id)
        )

        account = result.scalars().first()

        if account is None:
            raise HTTPException(
                status_code=404,
                detail="Item not found",
            )

        if (account.version + 1) != version:
            e = BusinessValidationError()
            e.add_error(
                "inconsistent_version",
                (
                    "The new version number must be greater than ",
                    "the current version number by exactly 1.",
                ),
                None,
            )
            raise e

        if account.balance + amount < 0:
            e = BusinessValidationError()
            e.add_error(
                "negative_balance",
                "The transaction would result in a negative balance.",
                None,
            )
            raise e

        account.version = version
        account.balance += amount
        await db.commit()
        await db.refresh(account)
        return account
    except SQLAlchemyError as sqlae:
        await db.rollback()
        raise AppServiceError(
            "Failed to update an account.",
            {"msg": str(sqlae)},
        ) from sqlae


async def get_account_by_user(db: AsyncSession, user_id: Uuid):
    return await get_object(
        db,
        select(DbAccount).where(
            DbAccount.user_id == user_id,
        ),
    )
