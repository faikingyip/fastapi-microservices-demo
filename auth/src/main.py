import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.db.database import db_manager
from src.middlewares import mw_error_handler, mw_req_duration
from src.routes import rt_refresh, rt_signin, rt_signup, rt_user

# from fastapi.staticfiles import StaticFiles


def load_env():
    # ENV is set in conftest.py
    env = os.environ.get("ENV", "Development")
    if env == "Testing":
        load_dotenv(".env.test")
    else:
        load_dotenv(".env.dev")


load_env()
db_host = os.environ.get("DB_HOST")
db_port = os.environ.get("DB_PORT")
db_name = os.environ.get("DB_NAME")
db_user = os.environ.get("DB_USER")
db_pass = os.environ.get("DB_PASS")
DATABASE_URL = f"postgresql+asyncpg://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"
db_manager.setup(DATABASE_URL)


app = FastAPI(title="FastAPI Microservices Demo")
app.include_router(rt_signup.router)
app.include_router(rt_signin.router)
app.include_router(rt_refresh.router)
app.include_router(rt_user.router)


# Configure logging
# configure_logging()

# allow_origins = ["http://localhost:5173"]
allow_origins = ["*"]
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
