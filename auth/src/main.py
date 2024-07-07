from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.db.database import Base, engine
from src.middlewares import mw_error_handler, mw_req_duration
from src.routes import rt_signup

# from src.routes import rt_user


# from fastapi.staticfiles import StaticFiles


async def create_database_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up")
    await create_database_tables()
    yield
    print("Shutting down")


app = FastAPI(title="Codefrantic API", lifespan=lifespan)
# app.include_router(rt_user.router)
app.include_router(rt_signup.router)


# Configure logging
# configure_logging()

allow_origins = ["http://localhost:5173"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(
    Exception,
    mw_error_handler.handle_error,
)

app.middleware("http")(mw_req_duration.request_duration)

# app.add_middleware(LoggingMiddleware)

# app.mount("/d_content", StaticFiles(directory="src/d_content"), name="d_content")
