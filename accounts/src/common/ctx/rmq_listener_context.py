import time

from src.common.ctx.db_manager import DbManager
from src.common.ctx.rmq_listener_client import RMQListenerClient


class RMQListenerContext:
    """The context used for running RMQ listeners,
    which should be run in a different thread from the
    FastAPI context. The context holds various components
    required in order to run the RMQ listeners required for
    this service. This context should be a singleton -
    only one instance should be run throughout the lifetime
    of the application."""

    instance = None

    def __init__(self):
        self.db_man: DbManager = DbManager()
        self.rmq_listener_client: RMQListenerClient = RMQListenerClient()

    def ensure_db_conn(self):
        db_available = False
        print("ENSURING DB AVAILABLE")
        while not db_available:
            db_available = self.db_man.check_conn()
            if not db_available:
                time.sleep(2)
        print("DB AVAILABLE!")

    def ensure_rmq_listener_client_conn(self):
        rmq_available = False
        print("ENSURING RMQ LISTENER CLIENT AVAILABLE")
        while not rmq_available:
            rmq_available = self.rmq_listener_client.check_conn()
            if not rmq_available:
                time.sleep(3)
        print("RMQ LISTENER CLIENT AVAILABLE!")

    @staticmethod
    def get_instance():
        if not RMQListenerContext.instance:
            RMQListenerContext.instance = RMQListenerContext()
        return RMQListenerContext.instance
