import time

from src.common.ctx.ctx_components import AbstractDbManager, AbstractMsgPublisherClient


class ApiContext:
    """An ApiContext holds all the the main components
    that are needed to run a FastAPI application.
    It also exposes some convenient methods to ensure
    the components required are operational.
    The ApiContext should be a singleton - only one
    instance should be created throughout the entire
    application lifetime."""

    instance = None

    def __init__(self):
        self.db_man: AbstractDbManager = None
        self.msg_pub_client: AbstractMsgPublisherClient = None

    def ensure_db_conn(self):
        db_available = False
        print("ENSURING DB AVAILABLE IN API CONTEXT")
        while not db_available:
            try:
                db_available = self.db_man.check_conn()
            except Exception:
                time.sleep(3)
            if not db_available:
                time.sleep(2)
        print("DB AVAILABLE!")

    def ensure_msg_pub_client_conn(self):
        rmq_available = False
        print("ENSURING RMQ PUB CLIENT AVAILABLE")
        while not rmq_available:
            try:
                rmq_available = self.msg_pub_client.check_conn()
            except Exception:
                time.sleep(3)
            if not rmq_available:
                time.sleep(3)
        print("RMQ PUB CLIENT AVAILABLE!")

    @staticmethod
    def get_instance():
        if not ApiContext.instance:
            ApiContext.instance = ApiContext()
        return ApiContext.instance

    @staticmethod
    async def get_instance_async():
        return ApiContext.get_instance()
