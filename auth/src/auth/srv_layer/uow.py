import abc

from sqlalchemy.ext import asyncio

from src.auth.adapters import repo


class AbstractUoW(abc.ABC):

    def __init__(self):
        self.users: repo.AbstractUserRepo = None

    async def __aenter__(self) -> "AbstractUoW":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.rollback()

    @abc.abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def rollback(self):
        raise NotImplementedError

    @abc.abstractmethod
    async def refresh(self, new_record):
        raise NotImplementedError

    @abc.abstractmethod
    def expunge(self, record):
        raise NotImplementedError


class SqlAlchemyUoW(AbstractUoW):
    def __init__(
        self,
        session_factory: asyncio.async_sessionmaker,
    ):
        super().__init__()
        self.session_factory = session_factory
        self.session: asyncio.AsyncSession = None

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = repo.UserRepo(self.session)
        return await super().__aenter__()

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await super().__aexit__(exc_type, exc_val, exc_tb)
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def refresh(self, new_record):
        await self.session.refresh(new_record)

    def expunge(self, record):
        self.session.expunge(record)
