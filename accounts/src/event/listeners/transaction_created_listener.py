import asyncio
import json
import os

from src.common.database import DbManager
from src.common.rabbit_mq import RabbitMQClient
from src.constants.event_subject import EventSubjects
from src.ops import ops_account


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

    def on_message_received_handler(channel, method, properties, body):

        print(f"TRANSACTION:CREATED LISTENER: received new message: {body}")

        # async def call_update_account():
        #     async with db_man.SessionLocal() as db:
        #         try:
        #             return await ops_account.update_account(
        #                 db,
        #                 user_id=json.loads(body)["user_id"],
        #             )
        #         finally:
        #             await db.close()

        # loop.run_until_complete(call_update_account())

        channel.basic_ack(delivery_tag=method.delivery_tag)

    class TransactionCreatedListener:
        def __init__(self, client: RabbitMQClient):
            self.client: RabbitMQClient = client
            self.subject = EventSubjects.TRANSACTION_CREATED

        def listen(self):
            self.client.listen(self.subject, on_message_received_handler)

    TransactionCreatedListener(rmq_client).listen()
