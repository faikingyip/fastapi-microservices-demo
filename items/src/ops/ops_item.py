from typing import Any, Dict

from fastapi import Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.crud import get_objects
from src.db.models.db_item import DbItem

# async def get_user_by_id(db: AsyncSession, user_id: UUID):
#     try:
#         return (
#             await db.execute(
#                 select(DbItem).where(DbItem.id == user_id),
#             )
#         ).scalar_one_or_none()
#     except SQLAlchemyError as sqlae:
#         raise AppServiceError(
#             "Failed to get a user by id.",
#             {"msg": str(sqlae)},
#         ) from sqlae


async def get_items(
    db: AsyncSession, page_index: int, page_size: int, sort_by: str = Query(None)
) -> Dict[str, Any]:
    query = select(DbItem)
    return await get_objects(DbItem, db, query, page_index, page_size, sort_by)
