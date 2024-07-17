from asyncpg import UniqueViolationError
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


async def get_account_by_user(db: AsyncSession, user_id: Uuid):
    return await get_object(
        db,
        select(DbAccount).where(
            DbAccount.user_id == user_id,
        ),
    )
