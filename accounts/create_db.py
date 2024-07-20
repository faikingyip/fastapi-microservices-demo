import asyncio

from src.app import load_env
from src.common.api_context_builder import ApiContextBuilder
from src.common.database import Base
from src.db.models import db_account


async def create_db():
    load_env()
    api_ctx = ApiContextBuilder().config_db_man().ensure_db_conn().build()
    async with api_ctx.db_man.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await api_ctx.db_man.engine.dispose()


if __name__ == "__main__":
    asyncio.run(create_db())
