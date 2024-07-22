import pika

from src.common.rmq.rmq_client import RMQClient


class RMQPublisherClient(RMQClient):
    """A RMQ client specifically for publishing
    notification messages to the RMQ server.
    This client can run within the ApiContext
    as it does not require an ongoing connection
    to the RMQ server."""

    def __init__(self):
        super().__init__()

    def publish(self, routing_key, message):
        try:
            self.channel.basic_publish(
                exchange=self.exchange_name,
                routing_key=routing_key,
                body=message,
            )
        except pika.exceptions.AMQPConnectionError:
            # Logging
            pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    async def get_rmq_pub_client(self):
        return self
