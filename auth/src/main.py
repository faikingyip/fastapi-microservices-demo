import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.db.database import Base, engine
from src.routers import rt_user

# from fastapi.staticfiles import StaticFiles


async def create_database_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Startup things")
    # await create_database_tables()
    yield
    print("Shutdown things")


app = FastAPI(title="Codefrantic API", lifespan=lifespan)
app.include_router(rt_user.router)


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


# Add middleware
# app.add_middleware(LoggingMiddleware)


# Add a middleware to take the duration of a request
# and attach it to the header of the response.
@app.middleware("http")
async def request_duration(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    duration = time.time() - start_time
    response.headers["duration"] = str(duration)
    return response


# app.mount("/d_content", StaticFiles(directory="src/d_content"), name="d_content")
