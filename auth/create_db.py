import asyncio

from src.auth import bootstrap
from src.auth.domain import models
from src.auth.srv_layer.uow import SqlAlchemyUoW
from src.common.ctx.api_context import ApiContext
from src.common.db.base import Base


async def create_db():

    bootstrap.load_env()

    _db_man = bootstrap.build_db_man()
    bootstrap.bootstrap_api_ctx(
        db_man=_db_man,
        uow=SqlAlchemyUoW(_db_man.session_local),
        msg_pub_client=None,
    )

    api_ctx = ApiContext.get_instance()
    async with api_ctx.db_man.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await api_ctx.db_man.engine.dispose()


# if __name__ == "__main__":
asyncio.run(create_db())
