from threading import Thread

from src.app import app, config_db, config_rmq, load_env
from src.common.rabbit_mq import rmq_client
from src.event.listeners.user_created_listener import UserCreatedListener

load_env()
config_db()
config_rmq()


thread = Thread(target=UserCreatedListener(rmq_client).listen)
thread.start()
