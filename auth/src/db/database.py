from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

# DATABASE_URL = (
#     "postgresql+asyncpg://codefranticuser:codefranticuser@localhost:5432/codefrantic"
# )
DATABASE_URL = (
    "postgresql+asyncpg://myuser:mypassword@auth-pg-srv.default:5432/mydatabase"
)

# Create a database engine
engine = create_async_engine(DATABASE_URL)

# Declare a sessionmaker with autocommit and autoflush settings
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


async def get_db():
    async with SessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()
