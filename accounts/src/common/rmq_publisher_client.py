import pika
from pika.exchange_type import ExchangeType

from src.common.rmq_client import RMQClient


class RMQPublisherClient(RMQClient):
    def __init__(self):
        super().__init__()
        # self.connection = None
        # self.channel = None
        # self.url = None
        # self.exchange_name = None

    # def setup(
    #     self,
    #     rmq_host,
    #     rmq_port,
    #     rmq_user,
    #     rmq_pass,
    #     exchange_name,
    # ):
    #     self.url = f"amqp://{rmq_user}:{rmq_pass}@{rmq_host}:{rmq_port}"
    #     self.exchange_name = exchange_name

    # def connect(self):

    #     if self.connection and self.connection.is_open:
    #         return

    #     self.connection = pika.BlockingConnection(pika.URLParameters(self.url))
    #     self.channel = self.connection.channel()

    #     # Declare an exchange. The type is direct, which routes the message
    #     # to multiple queues based on the queue bindings.
    #     # Messages in each queue will be consumed by a TYPE of consumer.
    #     # channel.queue_declare(queue=queue_name)
    #     self.channel.exchange_declare(
    #         exchange=self.exchange_name,
    #         exchange_type=ExchangeType.direct,
    #     )

    def publish(self, routing_key, message):
        try:
            self.channel.basic_publish(
                exchange=self.exchange_name,
                routing_key=routing_key,
                body=message,
            )
        except pika.exceptions.AMQPConnectionError:
            # self.close()
            pass
        # finally:
        #     self.close()

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # def check_conn(self):

    #     if self.connection and self.connection.is_open:
    #         return True

    #     try:
    #         connection = pika.BlockingConnection(pika.URLParameters(self.url))
    #         connection.close()
    #         return True
    #     except pika.exceptions.AMQPConnectionError:
    #         return False

    async def get_rmq_pub_client(self):
        return self
