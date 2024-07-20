from src.common.api_context import ApiContext
from src.common.api_context_component_factory import ApiContextComponentFactory


class ApiContextBuilder:
    def __init__(self):
        self.api_ctx: ApiContext = ApiContext.get_instance()

    def config_db_man(self):
        ApiContextComponentFactory().config_db_man(self.api_ctx.db_man)
        return self

    def config_rmq_pub_client(self):
        ApiContextComponentFactory().config_rmq_pub_client(self.api_ctx.rmq_pub_client)
        return self

    def ensure_db_conn(self):
        self.api_ctx.ensure_db_conn()
        return self

    def ensure_rmq_pub_client_conn(self):
        self.api_ctx.ensure_rmq_pub_client_conn()
        return self

    def build(self):
        return self.api_ctx
