import asyncio

from src.app import config_db, db_manager, load_env
from src.common.database import Base


async def create_db():
    load_env()
    config_db()
    async with db_manager.engine.begin() as conn:
        from src.db.models import db_transaction

        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await db_manager.engine.dispose()


# if __name__ == "__main__":
asyncio.run(create_db())
