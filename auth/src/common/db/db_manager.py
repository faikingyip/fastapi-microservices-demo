import psycopg2
from sqlalchemy.ext import asyncio

from src.common.ctx.ctx_components import AbstractDbManager


class DbManager(AbstractDbManager):
    """Manages connections to the database."""

    def __init__(self):
        super().__init__()
        self.db_url = None
        self.engine = None
        self.session_local = None

        self.db_host = None
        self.db_port = None
        self.db_name = None
        self.db_user = None
        self.db_pass = None

    def setup(self, db_host, db_port, db_name, db_user, db_pass):
        self.db_url = (
            f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
        )
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_user = db_user
        self.db_pass = db_pass

        self.engine = asyncio.create_async_engine(
            self.db_url,
            # echo=True,
        )

        self.session_local = asyncio.async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine,
        )

    def check_conn(self):
        """Checks the connection to the database.
        Check is performed in sync mode."""
        try:
            conn = psycopg2.connect(
                host=self.db_host,
                port=self.db_port,
                dbname=self.db_name,
                user=self.db_user,
                password=self.db_pass,
                connect_timeout=3,
            )
            conn.close()
            return True
        except psycopg2.OperationalError:
            return False
        except Exception:
            return False

    async def get_session(self):
        async with self.session_local() as db:
            try:
                yield db
            finally:
                await db.close()
