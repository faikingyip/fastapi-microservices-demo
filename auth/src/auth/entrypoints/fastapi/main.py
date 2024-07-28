from src.auth import bootstrap
from src.auth.entrypoints.fastapi.app import app
from src.auth.srv_layer.uow import SqlAlchemyUoW

_ = app

bootstrap.load_env()

_db_man = bootstrap.build_db_man()
bootstrap.bootstrap_api_ctx(
    db_man=_db_man,
    uow=SqlAlchemyUoW(_db_man.session_local),
    msg_pub_client=bootstrap.build_rmq_pub_client(),
)
