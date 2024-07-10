from typing import Any, Dict

from fastapi import Query
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.db_item import DbItem
from src.db.query_utils import apply_sorting_and_paging_to_list_query
from src.errors import AppServiceError

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


# async def get_items(
#     db: AsyncSession, page_index: int, page_size: int, sort_by: str = Query(None)
# ):
#     query = select(DbItem)
#     query = apply_sorting_and_paging_to_list_query(
#         query, DbItem, page_index, page_size, sort_by
#     )
#     try:
#         results = await db.execute(query)
#         items = results.scalars().all()
#         return items
#     except SQLAlchemyError as sqlae:
#         raise AppServiceError(
#             "Failed to get items.",
#             {"msg": str(sqlae)},
#         ) from sqlae


async def get_items(
    db: AsyncSession, page_index: int, page_size: int, sort_by: str = Query(None)
) -> Dict[str, Any]:
    query = select(DbItem)
    query = apply_sorting_and_paging_to_list_query(
        query, DbItem, page_index, page_size, sort_by
    )

    total_items = 0
    try:
        # total_items = db.query(DbItem).count()
        # total_items_result = await db.execute(select([func.count(DbItem.id)]))
        total_items_result = await db.execute(select(func.count(DbItem.id)))
        total_items = total_items_result.scalar_one()
    except SQLAlchemyError as sqlae:
        raise AppServiceError(
            "Failed to get items.",
            {"msg": str(sqlae)},
        ) from sqlae

    items = None
    try:
        results = await db.execute(query)
        items = results.scalars().all()
    except SQLAlchemyError as sqlae:
        raise AppServiceError(
            "Failed to get items.",
            {"msg": str(sqlae)},
        ) from sqlae

    return {
        "items": items,
        "page_index": page_index,
        "page_size": page_size,
        "total_items": total_items,
        "items_in_page": len(items),
    }
