from src.auth import bootstrap
from src.auth.entrypoints.fastapi.app import app

_ = app

bootstrap.load_env()

bootstrap.bootstrap_api_ctx(
    db_man=bootstrap.build_db_man(),
    msg_pub_client=bootstrap.build_rmq_pub_client(),
)
