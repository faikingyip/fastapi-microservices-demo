import abc

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.domain import models


class AbstractUserRepo(abc.ABC):
    @abc.abstractmethod
    async def add(self, user: models.User):
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, id) -> models.User:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_by_email(self, email) -> models.User:
        raise NotImplementedError


class UserRepo(AbstractUserRepo):
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session

    async def add(self, user: models.User):
        self.session.add(user)
        await self.session.flush()

    async def get(self, id):
        query = select(models.User).where(
            models.User.id == id,
        )
        return (await self.session.execute(query)).scalar_one_or_none()

    async def get_by_email(self, email) -> models.User:
        query = select(models.User).where(
            models.User.email == email,
        )
        return (await self.session.execute(query)).scalar_one_or_none()
