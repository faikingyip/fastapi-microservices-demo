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
            echo=True,
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


# ============

# import os

# from dotenv import load_dotenv
# from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
# from sqlalchemy.orm import DeclarativeBase


# def load_env():
#     env = os.environ.get("ENV", "Development")

#     print(env)
#     print("sdgfdgdfgdfdsfdssdfdgdgdfgdfgfdgfdgfdfdgdfgfdgfdg")
#     if env == "Testing":
#         load_dotenv(".env.test")
#     else:
#         load_dotenv(".env.dev")


# load_env()

# db_host = os.environ.get("DB_HOST")
# db_port = os.environ.get("DB_PORT")
# db_name = os.environ.get("DB_NAME")
# db_user = os.environ.get("DB_USER")
# db_pass = os.environ.get("DB_PASS")


# # if not db_host:
# #     load_dotenv()
# #     db_host = os.environ.get("DB_HOST")
# #     db_port = os.environ.get("DB_PORT")
# #     db_name = os.environ.get("DB_NAME")
# #     db_user = os.environ.get("DB_USER")
# #     db_pass = os.environ.get("DB_PASS")


# DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

# # Create a database engine
# engine = create_async_engine(
#     DATABASE_URL,
#     echo=True,
# )

# # Declare a sessionmaker with autocommit and autoflush settings
# SessionLocal = async_sessionmaker(
#     autocommit=False,
#     autoflush=False,
#     bind=engine,
# )


# class Base(DeclarativeBase):
#     pass


# async def get_db():
#     async with SessionLocal() as db:
#         try:
#             yield db
#         finally:
#             await db.close()
