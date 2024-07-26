from asyncpg import UniqueViolationError
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from src.auth.domain import models
from src.auth.srv_layer import uow


class EmailTakenError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


async def signup(
    email: str,
    password: str,
    first_name: str,
    last_name: str,
    uow: uow.AbstractUoW,
) -> models.User:
    async with uow:
        try:
            users_man = models.UsersManager()
            user = users_man.signup(
                email,
                password,
                first_name,
                last_name,
            )
            await uow.users.add(user)
            await uow.commit()
            await uow.refresh(user)
            uow.expunge(user)
            return user
        except IntegrityError as ite:
            cause = ite.orig.__cause__
            if isinstance(cause, UniqueViolationError) and cause.detail.startswith(
                "Key (email)"
            ):
                raise EmailTakenError("Email is already in use.") from ite


async def signin(
    email: str,
    password: str,
    uow: uow.AbstractUoW,
) -> models.User:
    async with uow:
        user = await uow.users.get_by_email(email)
        if not user or not user.is_password_valid(password):
            raise InvalidCredentialsError("Invalid credentials")
        uow.expunge(user)
        return user


async def get_by_email(
    email: str,
    uow: uow.AbstractUoW,
) -> models.User:
    async with uow:
        user = await uow.users.get_by_email(email)
        uow.expunge(user)
        return user


def build_token_data(
    id: str,
    email: str,
    first_name: str,
    last_name: str,
) -> dict:
    return {
        "sub": email,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "user_id": str(id),
    }


def build_http_exc_401(
    detail,
):
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"},
    )
