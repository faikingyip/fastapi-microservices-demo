import os

from src.common.db_manager import DbManager
from src.common.rmq_listener_client import Listener, RMQListenerClient


class RMQListenerContextComponentFactory:
    def config_db_man(self, db_man: DbManager):
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

    def config_rmq_listener_client(
        self,
        rmq_listener_client: RMQListenerClient,
        listeners: list[Listener],
    ):
        rmq_host = os.environ.get("RABBITMQ_HOST")
        rmq_port = os.environ.get("RABBITMQ_PORT")
        rmq_user = os.environ.get("RABBITMQ_USER")
        rmq_pass = os.environ.get("RABBITMQ_PASS")
        exch_name = os.environ.get("RABBITMQ_EXHCANGE_NAME")
        # rmq_listener_client = RMQListenerClient()
        rmq_listener_client.setup(
            rmq_host,
            rmq_port,
            rmq_user,
            rmq_pass,
            exch_name,
        )
        rmq_listener_client.set_listeners(listeners)
        return rmq_listener_client
