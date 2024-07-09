import asyncio

from src.db.database import Base
from src.main import db_manager


async def create_db():
    async with db_manager.engine.begin() as conn:
        from src.db.models import db_user

        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await db_manager.engine.dispose()


# if __name__ == "__main__":
asyncio.run(create_db())
