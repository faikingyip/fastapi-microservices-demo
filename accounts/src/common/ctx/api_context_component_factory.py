import os

from src.common.ctx.db_manager import DbManager
from src.common.ctx.rmq_publisher_client import RMQPublisherClient


class ApiContextComponentFactory:
    """Builds the components that are required by
    the ApiContext."""

    def config_db_man(self, db_man: DbManager):
        """Sets up the DbManager for connecting
        to the database."""
        db_host = os.environ.get("DB_HOST")
        db_port = os.environ.get("DB_PORT")
        db_name = os.environ.get("DB_NAME")
        db_user = os.environ.get("DB_USER")
        db_pass = os.environ.get("DB_PASS")
        # db_man = DbManager()
        db_man.setup(
            db_host,
            db_port,
            db_name,
            db_user,
            db_pass,
        )
        return db_man

    def config_rmq_pub_client(self, rmq_pub_client: RMQPublisherClient):
        """Sets up the RMQ Publishing Client, required
        for connecting to RMQ for publishing
        notifications."""
        rmq_host = os.environ.get("RABBITMQ_HOST")
        rmq_port = os.environ.get("RABBITMQ_PORT")
        rmq_user = os.environ.get("RABBITMQ_USER")
        rmq_pass = os.environ.get("RABBITMQ_PASS")
        exch_name = os.environ.get("RABBITMQ_EXHCANGE_NAME")
        # rmq_pub_client = RMQPublisherClient()
        rmq_pub_client.setup(
            rmq_host,
            rmq_port,
            rmq_user,
            rmq_pass,
            exch_name,
        )
        return rmq_pub_client
