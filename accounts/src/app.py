"""This module sets up the FasiAPI application that are common to
the various initiation channels. Initiation channels include the
main.py, create_db.py, alembic env.py, and pytest. Each of these
initiation channels can subsequently perform tasks specific to
their area."""

import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.accounts import entrypoints
from src.middlewares import mw_error_handler, mw_req_duration


def load_env():
    """Loads environment variables from the
    initiation channels. You need to set the
    ENV variable (if appropriate), then call this function to
    load the correct settings."""

    # ENV can be set in places
    # such as conftest.py for pytest.
    env = os.environ.get("ENV")
    print(f"{env=}")
    if env == "Testing":
        load_dotenv(".env.test")
    elif env == "Production":
        # Do nothing here. Just let
        # the block exit and load the
        # already set environments
        # below.
        pass
    else:
        load_dotenv(".env.dev")


app = FastAPI(title="FastAPI Microservices Demo - Accounts service")
app.include_router(entrypoints.get_account.router)

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

# app.mount(
#     "/d_content",
#     StaticFiles(directory="src/d_content"),
#     name="d_content",
# )

# return app
