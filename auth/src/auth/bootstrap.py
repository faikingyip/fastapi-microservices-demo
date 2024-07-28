import os
from typing import Optional

from dotenv import load_dotenv

from src.common.ctx.api_context import ApiContext
from src.common.ctx.ctx_components import AbstractMsgPublisherClient
from src.common.db.db_manager import DbManager
from src.common.rmq.rmq_publisher_client import RMQPublisherClient


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


def build_db_man():
    """Sets up the DbManager for connecting
    to the database."""
    db_host = os.environ.get("DB_HOST")
    db_port = os.environ.get("DB_PORT")
    db_name = os.environ.get("DB_NAME")
    db_user = os.environ.get("DB_USER")
    db_pass = os.environ.get("DB_PASS")
    db_man = DbManager()
    db_man.setup(
        db_host,
        db_port,
        db_name,
        db_user,
        db_pass,
    )
    return db_man


def build_rmq_pub_client():
    """Sets up the RMQ Publishing Client, required
    for connecting to RMQ for publishing
    notifications."""
    rmq_host = os.environ.get("RABBITMQ_HOST")
    rmq_port = os.environ.get("RABBITMQ_PORT")
    rmq_user = os.environ.get("RABBITMQ_USER")
    rmq_pass = os.environ.get("RABBITMQ_PASS")
    exch_name = os.environ.get("RABBITMQ_EXHCANGE_NAME")
    msg_pub_client = RMQPublisherClient()
    msg_pub_client.setup(
        rmq_host,
        rmq_port,
        rmq_user,
        rmq_pass,
        exch_name,
    )
    return msg_pub_client


def bootstrap_api_ctx(
    db_man: DbManager,
    msg_pub_client: Optional[AbstractMsgPublisherClient],
):
    api_ctx = ApiContext.get_instance()
    api_ctx.db_man = db_man
    api_ctx.ensure_db_conn()
    if msg_pub_client:
        api_ctx.msg_pub_client = msg_pub_client
        api_ctx.ensure_msg_pub_client_conn()
