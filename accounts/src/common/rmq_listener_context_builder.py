from src.common.rmq_listener_client import Listener
from src.common.rmq_listener_context import RMQListenerContext
from src.common.rmq_listener_context_component_factory import (
    RMQListenerContextComponentFactory,
)


class RMQListenerContextBuilder:
    def __init__(self):
        self.rmq_listener_ctx: RMQListenerContext = RMQListenerContext.get_instance()

    def config_db_man(self):
        RMQListenerContextComponentFactory().config_db_man(
            self.rmq_listener_ctx.db_man,
        )
        return self

    def config_rmq_listener_client(self, listeners: list[Listener]):
        RMQListenerContextComponentFactory().config_rmq_listener_client(
            self.rmq_listener_ctx.rmq_listener_client, listeners
        )
        return self

    def ensure_db_conn(self):
        self.rmq_listener_ctx.ensure_db_conn()
        return self

    def ensure_rmq_listener_client_conn(self):
        self.rmq_listener_ctx.ensure_rmq_listener_client_conn()
        return self

    def build(self):
        return self.rmq_listener_ctx
