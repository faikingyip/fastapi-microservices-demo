from src.common.rabbit_mq import RabbitMQClient
from src.constants.event_subject import EventSubjects


def on_message_received_handler(channel, method, properties, body):
    print(f"LISTENER: received new message: {body}")
    channel.basic_ack(delivery_tag=method.delivery_tag)


class UserCreatedListener:
    def __init__(self, client: RabbitMQClient):
        self.client: RabbitMQClient = client
        self.subject = EventSubjects.USER_CREATED

    def listen(self):
        self.client.listen(self.subject, on_message_received_handler)
