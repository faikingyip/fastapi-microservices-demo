from asyncpg import UniqueViolationError
from sqlalchemy.exc import IntegrityError

from src.accounts.domain import models
from src.accounts.srv_layer import uow


class UserAlreadyHasAccountError(Exception):
    pass


async def create_account(
    user_id: str,
    uow: uow.AbstractUoW,
) -> models.Account:
    async with uow:
        try:
            accs_man = models.AccountsManager()
            account = accs_man.create_account(user_id)
            await uow.accounts.add(account)
            await uow.commit()
            await uow.refresh(account)
            uow.expunge(account)
            return account
        except IntegrityError as ite:
            cause = ite.orig.__cause__
            if isinstance(cause, UniqueViolationError) and cause.detail.startswith(
                "Key (user_id)"
            ):
                raise UserAlreadyHasAccountError(
                    "Email is already in use.",
                ) from ite


async def get_by_user(
    user_id: str,
    uow: uow.AbstractUoW,
) -> models.Account:
    async with uow:
        account = await uow.accounts.get_by_user(user_id)
        uow.expunge(account)
        return account
