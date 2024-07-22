from uuid import UUID

from asyncpg import UniqueViolationError
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.models.db_user import DbUser
from src.errors import AppServiceError, BusinessValidationError
from src.schemas.schema_user import SchemaUserCreate
from src.utils import hash as h


async def create_user(
    db: AsyncSession,
    request: SchemaUserCreate,
):
    new_record = DbUser(
        email=request.email,
        password_hash=h.bcrypt(request.password),
        first_name=request.first_name,
        last_name=request.last_name,
    )
    try:
        db.add(new_record)
        await db.commit()
        await db.refresh(new_record)
    except IntegrityError as ite:
        await db.rollback()
        cause = ite.orig.__cause__
        if isinstance(cause, UniqueViolationError) and cause.detail.startswith(
            "Key (email)"
        ):
            e = BusinessValidationError()
            e.add_error("unique_email", "Email is already in use.", None)
            raise e from ite
        raise AppServiceError(
            "Failed to create a user.",
            {"msg": str(ite)},
        ) from ite
    except SQLAlchemyError as sqlae:
        await db.rollback()
        raise AppServiceError(
            "Failed to create a user.",
            {"msg": str(sqlae)},
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
            {"msg": str(sqlae)},
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
            {"msg": str(sqlae)},
        ) from sqlae


# async def change_password(
#     db: AsyncSession,
#     user_id,
#     request: SchemaChangePassword,
# ):
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
#     db: AsyncSession,
#     page_index: int,
#     page_size: int,
#     sort_by: str = Query(None),
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
