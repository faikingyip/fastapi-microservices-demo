import asyncio
import json
import os
from threading import Thread

from src.app import app, config_db, config_rmq, load_env
from src.common.database import DbManager
from src.common.rabbit_mq import Listener, RabbitMQClient, rmq_client
from src.constants.event_subject import EventSubjects

# from src.event.listeners.user_created_listener import configure
from src.ops import ops_account

load_env()
config_db()
config_rmq()


def configure(rmq_client):

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    db_man = DbManager()
    db_host = os.environ.get("DB_HOST")
    db_port = os.environ.get("DB_PORT")
    db_name = os.environ.get("DB_NAME")
    db_user = os.environ.get("DB_USER")
    db_pass = os.environ.get("DB_PASS")
    db_man.setup(
        db_host,
        db_port,
        db_name,
        db_user,
        db_pass,
    )

    def on_user_created_message_received_handler(channel, method, properties, body):

        print(f"USER LISTENER: received new message: {body}")

        async def call_create_account():
            async with db_man.SessionLocal() as db:
                try:
                    return await ops_account.create_account(
                        db,
                        user_id=json.loads(body)["user_id"],
                    )
                finally:
                    await db.close()

        loop.run_until_complete(call_create_account())

        channel.basic_ack(delivery_tag=method.delivery_tag)

    def on_transaction_created_message_received_handler(
        channel, method, properties, body
    ):

        print(f"TRANS LISTENER: received new message: {body}")

        # async def call_create_account():
        #     async with db_man.SessionLocal() as db:
        #         try:
        #             return await ops_account.create_account(
        #                 db,
        #                 user_id=json.loads(body)["user_id"],
        #             )
        #         finally:
        #             await db.close()

        # loop.run_until_complete(call_create_account())

        channel.basic_ack(delivery_tag=method.delivery_tag)

    class RabbitMQListener:
        def __init__(self, client: RabbitMQClient):
            self.client: RabbitMQClient = client

        def listen(self, listners):
            self.client.listen(listners)

    listeners = [
        Listener(EventSubjects.USER_CREATED, on_user_created_message_received_handler),
        Listener(
            EventSubjects.TRANSACTION_CREATED,
            on_transaction_created_message_received_handler,
        ),
    ]
    RabbitMQListener(rmq_client).listen(listeners)


thread = Thread(target=configure, args=[rmq_client])
thread.start()
