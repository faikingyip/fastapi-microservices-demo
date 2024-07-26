import abc

from sqlalchemy.ext import asyncio

from src.accounts.adapters import repo
from src.common.ctx.api_context import ApiContext


class AbstractUoW(abc.ABC):

    def __init__(self):
        self.accounts: repo.AbstractAccountRepo = None

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


# DEFAULT_SESSION_FACTORY = sessionmaker(
#     bind=create_engine(
#         config.get_postgres_uri(),
#         isolation_level="REPEATABLE READ",
#     )
# )

DEFAULT_SESSION_FACTORY = ApiContext.get_instance().db_man.session_local


class SqlAlchemyUoW(AbstractUoW):
    def __init__(
        self,
        session_factory: asyncio.async_sessionmaker = DEFAULT_SESSION_FACTORY,
    ):
        super().__init__()
        self.session_factory = session_factory
        self.session: asyncio.AsyncSession = None

    async def __aenter__(self):
        self.session = self.session_factory()
        self.accounts = repo.AccountRepo(self.session)
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
