import pika
from pika.exchange_type import ExchangeType


class RabbitMQClient:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.exchange_name = None
        self.subject = None

    def setup(self, url, exchange_name):
        self.connection = pika.BlockingConnection(pika.URLParameters(url))
        self.channel = self.connection.channel()
        self.exchange_name = exchange_name

        # Declare an exchange. The type is direct, which routes the message
        # to multiple queues based on the queue bindings.
        # Messages in each queue will be consumed by a TYPE of consumer.
        # channel.queue_declare(queue=queue_name)
        self.channel.exchange_declare(
            exchange=self.exchange_name,
            exchange_type=ExchangeType.direct,
        )

    def publish(self, routing_key, message):
        self.channel.basic_publish(
            exchange=self.exchange_name,
            routing_key=routing_key,
            body=message,
        )

    def close(self):
        self.channel.close()
        self.connection.close()


rmq_client = RabbitMQClient()


async def get_rmq():
    return rmq_client
