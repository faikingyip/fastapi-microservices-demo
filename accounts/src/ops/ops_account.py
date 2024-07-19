import decimal

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
        result = await db.execute(
            select(DbAccount).filter(DbAccount.user_id == user_id)
        )

        tran = result.scalars().first()

        if tran is None:
            raise HTTPException(
                status_code=404,
                detail="Item not found",
            )

        if (tran.version + 1) != request["version"]:
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

        tran.version = request["version"]
        tran.balance += request["balance"]
        await db.commit()
        await db.refresh(tran)
        return tran
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
