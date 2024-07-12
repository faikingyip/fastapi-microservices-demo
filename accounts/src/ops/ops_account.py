from sqlalchemy import Uuid, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.crud import get_object
from src.db.models.db_account import DbAccount
from src.schemas.schema_account import SchemaAccountCreate


async def create_account(
    db: AsyncSession,
    request: SchemaAccountCreate,
):
    # new_record = DbAccount(
    #     title=request.title,
    #     description=request.description,
    #     price=request.price,
    # )
    # try:
    #     db.add(new_record)
    #     await db.commit()
    #     await db.refresh(new_record)
    # except IntegrityError as ite:
    #     await db.rollback()
    #     cause = ite.orig.__cause__
    #     if isinstance(cause, UniqueViolationError) and cause.detail.startswith(
    #         "Key (title)"
    #     ):
    #         e = BusinessValidationError()
    #         e.add_error("unique_email", "Title is already in use.", None)
    #         raise e from ite
    #     raise AppServiceError(
    #         "Failed to create an item.",
    #         {"msg": str(ite)},
    #     ) from ite
    # except SQLAlchemyError as sqlae:
    #     await db.rollback()
    #     raise AppServiceError(
    #         "Failed to create an item.",
    #         {"msg": str(sqlae)},
    #     ) from sqlae
    # return new_record
    pass


async def get_account_by_user(db: AsyncSession, user_id: Uuid):
    return await get_object(
        db,
        select(DbAccount).where(
            DbAccount.user_id == user_id,
        ),
    )
