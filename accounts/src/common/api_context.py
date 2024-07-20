import time

from src.common.db_manager import DbManager
from src.common.rmq_publisher_client import RMQPublisherClient


class ApiContext:
    instance = None

    def __init__(self):
        self.db_man: DbManager = DbManager()
        self.rmq_pub_client: RMQPublisherClient = RMQPublisherClient()

    def ensure_db_conn(self):
        db_available = False
        print("ENSURING DB AVAILABLE")
        while not db_available:
            db_available = self.db_man.check_conn()
            if not db_available:
                time.sleep(2)
        print("DB AVAILABLE!")

    def ensure_rmq_pub_client_conn(self):
        rmq_available = False
        print("ENSURING RMQ PUB CLIENT AVAILABLE")
        while not rmq_available:
            rmq_available = self.rmq_pub_client.check_conn()
            if not rmq_available:
                time.sleep(3)
        print("RMQ PUB CLIENT AVAILABLE!")

    @staticmethod
    def get_instance():
        if not ApiContext.instance:
            ApiContext.instance = ApiContext()
        return ApiContext.instance


def get_db_session_fn():
    if not ApiContext.get_instance().db_man:
        return None
    else:
        return ApiContext.get_instance().db_man.get_session
