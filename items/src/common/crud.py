from typing import Any, Dict

from fastapi import Query
from sqlalchemy import Uuid, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.common.query_utils import apply_sorting_and_paging_to_list_query
from src.errors import AppServiceError


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

    query = apply_sorting_and_paging_to_list_query(
        query, model_class, page_index, page_size, sort_by
    )

    total_items = 0
    try:
        total_items_result = await db.execute(
            select(func.count(model_class.id)),
        )
        total_items = total_items_result.scalar_one()
    except SQLAlchemyError as sqlae:
        raise AppServiceError(
            "Failed to get objects.",
            {"msg": str(sqlae)},
        ) from sqlae

    objects = None
    try:
        results = await db.execute(query)
        objects = results.scalars().all()
    except SQLAlchemyError as sqlae:
        raise AppServiceError(
            "Failed to get objects.",
            {"msg": str(sqlae)},
        ) from sqlae

    return {
        "items": objects,
        "page_index": page_index,
        "page_size": page_size,
        "total_items": total_items,
        "items_in_page": len(objects),
    }


async def get_object(
    db: AsyncSession,
    query: Query,
):
    """Pass in a query to return a single object.
    Query i.e. select(DbItem).where(DbItem.id == id)"""
    try:
        return (await db.execute(query)).scalar_one_or_none()
    except SQLAlchemyError as sqlae:
        raise AppServiceError(
            "Failed to get an object.",
            {"msg": str(sqlae)},
        ) from sqlae
