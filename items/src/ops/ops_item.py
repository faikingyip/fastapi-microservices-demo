from typing import Any, Dict

from asyncpg import UniqueViolationError
from fastapi import Query
from sqlalchemy import Uuid, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.crud import get_object, get_objects
from src.db.models.db_item import DbItem
from src.errors import AppServiceError, BusinessValidationError
from src.schemas.schema_item import SchemaItemCreate


async def create_item(
    db: AsyncSession,
    request: SchemaItemCreate,
):
    new_record = DbItem(
        title=request.title,
        description=request.description,
        price=request.price,
    )
    try:
        db.add(new_record)
        await db.commit()
        await db.refresh(new_record)
    except IntegrityError as ite:
        await db.rollback()
        cause = ite.orig.__cause__
        if isinstance(cause, UniqueViolationError) and cause.detail.startswith(
            "Key (title)"
        ):
            e = BusinessValidationError()
            e.add_error("unique_email", "Title is already in use.", None)
            raise e from ite
        raise AppServiceError(
            "Failed to create an item.",
            {"msg": str(ite)},
        ) from ite
    except SQLAlchemyError as sqlae:
        await db.rollback()
        raise AppServiceError(
            "Failed to create an item.",
            {"msg": str(sqlae)},
        ) from sqlae
    return new_record


async def get_items(
    db: AsyncSession, page_index: int, page_size: int, sort_by: str = Query(None)
) -> Dict[str, Any]:
    query = select(DbItem)
    return await get_objects(DbItem, db, query, page_index, page_size, sort_by)


# async def get_item(db: AsyncSession, id: Uuid):
#     try:
#         return (
#             await db.execute(
#                 select(DbItem).where(DbItem.id == id),
#             )
#         ).scalar_one_or_none()
#     except SQLAlchemyError as sqlae:
#         raise AppServiceError(
#             "Failed to get a object by id.",
#             {"msg": str(sqlae)},
#         ) from sqlae


async def get_item(db: AsyncSession, id: Uuid):
    return await get_object(db, select(DbItem).where(DbItem.id == id))
