from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.models.db_user import DbUser
from src.errors import AppServiceError
from src.schemas.schema_user import SchemaUserCreate
from src.utils import hash as h


async def create_user(
    db: AsyncSession,
    request: SchemaUserCreate,
):
    new_record = DbUser(
        email=request.email,
        password_hash=h.bcrypt(request.password),
    )
    try:
        db.add(new_record)
        await db.commit()
        await db.refresh(new_record)
    except SQLAlchemyError as sqlae:
        await db.rollback()
        raise AppServiceError(
            "Failed to create a user.",
            {},
        ) from sqlae
    return new_record


async def get_user_by_id(db: AsyncSession, user_id: UUID):
    try:
        return (
            await db.execute(
                select(DbUser).where(DbUser.id == user_id),
            )
        ).scalar_one_or_none()
    except SQLAlchemyError as sqlae:
        raise AppServiceError(
            "Failed to get a user by id.",
            {"user_id": user_id},
        ) from sqlae


async def get_user_by_email(db: AsyncSession, email: str):
    try:
        return (
            await db.execute(
                select(DbUser).where(DbUser.email == email),
            )
        ).scalar_one_or_none()
    except SQLAlchemyError as sqlae:
        raise AppServiceError(
            "Failed to get a user by email.",
            {"email": email},
        ) from sqlae


# async def change_password(db: AsyncSession, user_id, request: SchemaChangePassword):
#     stmt = (
#         update(DbUser)
#         .where(DbUser.id == user_id)
#         .values(password_hash=h.bcrypt(request.new_password))
#     )
#     rowcount = 0
#     try:
#         rowcount = (await db.execute(stmt)).rowcount
#         await db.commit()
#     except SQLAlchemyError as sqlae:
#         await db.rollback()
#         raise ChangePasswordError(sqlae) from sqlae
#     if rowcount != 1:
#         raise ChangePasswordError("Invalid credentials")
#     return rowcount


# async def get_users(
#     db: AsyncSession, page_index: int, page_size: int, sort_by: str = Query(None)
# ):
#     query = select(DbUser)
#     query = apply_sorting_and_paging_to_list_query(
#         query, DbUser, page_index, page_size, sort_by
#     )
#     try:
#         results = await db.execute(query)
#         users = results.scalars().all()
#         return users
#     except SQLAlchemyError as sqlae:
#         raise GetUserListError(sqlae) from sqlae

# async def delete_user(db: AsyncSession, user_id):
#     stmt = delete(DbUser).where(DbUser.id == user_id)
#     rowcount = 0
#     try:
#         rowcount = (await db.execute(stmt)).rowcount
#         await db.commit()
#     except SQLAlchemyError as sqlae:
#         await db.rollback()
#         raise DeleteUserError(sqlae) from sqlae
#     if rowcount != 1:
#         raise DeleteUserError("User not found")
#     return rowcount
