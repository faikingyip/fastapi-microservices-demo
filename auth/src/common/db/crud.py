from typing import Any, Dict

from fastapi import Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.db import query_paging_utils as qp


async def create_multiple(
    model_class,
    objects_data: list[any],
    db_session: AsyncSession,
):
    """Provide a list of db model objects and this function will
    add them and commit to the database."""
    objects = [model_class(**object_data) for object_data in objects_data]
    db_session.add_all(objects)
    await db_session.commit()
    return objects


async def get_objects(
    model_class,
    db: AsyncSession,
    query: Query,
    page_index: int,
    page_size: int,
    sort_by: str = Query(None),
) -> Dict[str, Any]:
    """Reusuable function to standardize retrieving
    a list of objects from the database, with pagination."""

    query = qp.apply_sorting_and_paging_to_list_query(
        query, model_class, page_index, page_size, sort_by
    )

    total_items_result = await db.execute(
        select(func.count(model_class.id)),
    )
    total_items = total_items_result.scalar_one()

    results = await db.execute(query)
    objects = results.scalars().all()

    return {
        "items": objects,
        "page_index": page_index,
        "page_size": page_size,
        "total_items": total_items,
        "items_in_page": len(objects),
    }
