import asyncio

from src.app import load_env
from src.auth import bootstrap
from src.auth.domain import models
from src.common.ctx.api_context import ApiContext
from src.common.db.base import Base


async def create_db():

    load_env()

    bootstrap.bootstrap_api_ctx(
        db_man=bootstrap.build_db_man(),
        msg_pub_client=None,
    )

    api_ctx = ApiContext.get_instance()
    async with api_ctx.db_man.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await api_ctx.db_man.engine.dispose()


# if __name__ == "__main__":
asyncio.run(create_db())
