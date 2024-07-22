from src.app import app, load_env
from src.common.ctx.api_context_builder import ApiContextBuilder

load_env()

(
    ApiContextBuilder()
    .config_db_man()
    .config_rmq_pub_client()
    .ensure_db_conn()
    .ensure_rmq_pub_client_conn()
    .build()
)
