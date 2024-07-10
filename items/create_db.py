import asyncio

from src.app import config_db, db_manager
from src.db.database import Base


async def create_db():
    config_db()
    async with db_manager.engine.begin() as conn:
        from src.db.models import db_item

        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await db_manager.engine.dispose()


# if __name__ == "__main__":
asyncio.run(create_db())
