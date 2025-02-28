from src.common.ctx import api_context_component_factory as ccf
from src.common.ctx.api_context import ApiContext


class ApiContextBuilder:
    """Provides the builder methods for
    configuing the components of the ApiContext.
    Depending on the run mode of the application,
    i.e. test, or prod, some of the components may
    not be needed."""

    def __init__(self):
        self.api_ctx: ApiContext = ApiContext.get_instance()

    def config_db_man(self):
        ccf.ApiContextComponentFactory().config_db_man(
            self.api_ctx.db_man,
        )
        return self

    def config_rmq_pub_client(self):
        ccf.ApiContextComponentFactory().config_rmq_pub_client(
            self.api_ctx.rmq_pub_client,
        )
        return self

    def ensure_db_conn(self):
        self.api_ctx.ensure_db_conn()
        return self

    def ensure_rmq_pub_client_conn(self):
        self.api_ctx.ensure_rmq_pub_client_conn()
        return self

    def build(self):
        return self.api_ctx
