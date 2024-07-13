from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class DbManager:
    def __init__(self):
        self.db_url = None
        self.engine = None
        self.SessionLocal = None

    def setup(self, db_url):
        self.db_url = db_url

        self.engine = create_async_engine(
            self.db_url,
            # echo=True,
        )

        self.SessionLocal = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )


db_manager = DbManager()


async def get_db():
    async with db_manager.SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
