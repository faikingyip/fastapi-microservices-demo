from src.app import app, load_env
from src.auth import bootstrap

load_env()


bootstrap.bootstrap_api_ctx(
    db_man=bootstrap.build_db_man(),
    msg_pub_client=bootstrap.build_rmq_pub_client(),
)


# (
#     ApiContextBuilder()
#     .config_db_man(DbManager())
#     .config_msg_pub_client()
#     .ensure_db_conn()
#     .ensure_msg_pub_client_conn()
#     .build()
# )
