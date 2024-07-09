import asyncio

from src.db.database import Base, engine


async def create_db():
    async with engine.begin() as conn:
        from src.db.models import db_user

        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()


# if __name__ == "__main__":
asyncio.run(create_db())
