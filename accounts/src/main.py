import asyncio
import time
from threading import Thread

from src.app import app, load_env
from src.common.ctx import rmq_listener_context_builder as rmqlcb
from src.common.ctx.api_context_builder import ApiContextBuilder
from src.common.ctx.rmq_listener_context import RMQListenerContext
from src.common.rmq.rmq_listener_client import Listener
from src.constants.event_subject import EventSubjects
from src.event.listeners import listeners
from src.ops import ops_account

load_env()

(
    ApiContextBuilder()
    .config_db_man()
    .config_rmq_pub_client()
    .ensure_db_conn()
    .ensure_rmq_pub_client_conn()
    .build()
)


def start_rmq_listener():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    (
        rmqlcb.RMQListenerContextBuilder()
        .config_db_man()
        .config_rmq_listener_client(
            listeners=[
                Listener(
                    EventSubjects.USER_CREATED,
                    listeners.create_user_created_message_received_handler(
                        RMQListenerContext.get_instance(), ops_account, loop
                    ),
                ),
                Listener(
                    EventSubjects.TRANSACTION_CREATED,
                    listeners.create_tran_created_msg_received_hndlr(
                        RMQListenerContext.get_instance(), ops_account, loop
                    ),
                ),
            ],
        )
        .ensure_db_conn()
        .ensure_rmq_listener_client_conn()
        .build()
        .rmq_listener_client.listen()
    )


thread = Thread(target=start_rmq_listener)
thread.start()
