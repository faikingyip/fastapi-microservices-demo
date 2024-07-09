from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker


class CRUD:
    async def get_all(self, async_session: async_sessionmaker[AsyncSession]):
        async with async_session() as session:
            statement = select(Note).order_by(Note.id)
