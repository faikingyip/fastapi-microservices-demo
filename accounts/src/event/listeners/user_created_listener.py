import asyncio
import json

from src.common.database import get_db
from src.common.rabbit_mq import RabbitMQClient
from src.constants.event_subject import EventSubjects
from src.ops import ops_account


def on_message_received_handler(channel, method, properties, body):

    print(f"LISTENER: received new message: {body}")

    async def call_create_account(get_db):
        async for db in get_db():
            return await ops_account.create_account(
                db,
                user_id=json.loads(body)["user_id"],
            )

    account = asyncio.run(call_create_account(get_db))
    print(account)
    channel.basic_ack(delivery_tag=method.delivery_tag)


class UserCreatedListener:
    def __init__(self, client: RabbitMQClient):
        self.client: RabbitMQClient = client
        self.subject = EventSubjects.USER_CREATED

    def listen(self):
        self.client.listen(self.subject, on_message_received_handler)
