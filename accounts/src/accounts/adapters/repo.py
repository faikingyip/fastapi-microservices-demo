import abc

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.accounts.domain import models


class AbstractAccountRepo(abc.ABC):
    @abc.abstractmethod
    async def add(self, account: models.Account):
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, id) -> models.Account:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_user(self, user_id) -> models.Account:
        raise NotImplementedError


class AccountRepo(AbstractAccountRepo):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def add(self, account: models.Account):
        self.session.add(account)
        await self.session.flush()

    async def get(self, id):
        query = select(models.Account).where(
            models.Account.id == id,
        )
        return (await self.session.execute(query)).scalar_one_or_none()

    async def get_by_user(self, user_id):
        query = select(models.Account).where(
            models.Account.user_id == user_id,
        )
        return (await self.session.execute(query)).scalar_one_or_none()
