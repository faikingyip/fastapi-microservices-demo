"""This module sets up the FastAPI application that are common to
the various initiation channels. Initiation channels include the 
main.py, create_db.py, alembic env.py, and pytest. Each of these
initiation channels can subsequently perform tasks specific to
their area."""

import os
import time

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.common.database import db_manager
from src.common.rabbit_mq import rmq_client
from src.middlewares import mw_error_handler, mw_req_duration
from src.routes import rt_create_transaction, rt_get_transaction, rt_get_transactions


def load_env():
    """Function to load environment variables from the
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

    # Environment variables will either be sourced
    # from .env files or they will already exist
    # when building the environment.


def config_db():

    db_host = os.environ.get("DB_HOST")
    db_port = os.environ.get("DB_PORT")
    db_name = os.environ.get("DB_NAME")
    db_user = os.environ.get("DB_USER")
    db_pass = os.environ.get("DB_PASS")
    db_manager.setup(
        db_host,
        db_port,
        db_name,
        db_user,
        db_pass,
    )

    db_available = False
    while not db_available:
        db_available = db_manager.check_conn()
        if not db_available:
            print("DB not yet available")
            time.sleep(1)
    print("DB AVAILABLE!")


def config_rmq():
    rmq_host = os.environ.get("RABBITMQ_HOST")
    rmq_port = os.environ.get("RABBITMQ_PORT")
    rmq_user = os.environ.get("RABBITMQ_USER")
    rmq_pass = os.environ.get("RABBITMQ_PASS")
    exch_name = os.environ.get("RABBITMQ_EXHCANGE_NAME")
    rmq_url = f"amqp://{rmq_user}:{rmq_pass}@{rmq_host}:{rmq_port}"
    print(f"{rmq_url=}")
    rmq_client.setup(rmq_url, exch_name)

    rmq_available = False
    while not rmq_available:
        rmq_available = rmq_client.check_conn()
        if not rmq_available:
            print("RMQ not yet available")
            time.sleep(3)
    print("RMQ AVAILABLE!")


app = FastAPI(title="FastAPI Microservices Demo - transactions service")
app.include_router(rt_get_transactions.router)
app.include_router(rt_get_transaction.router)
app.include_router(rt_create_transaction.router)


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
