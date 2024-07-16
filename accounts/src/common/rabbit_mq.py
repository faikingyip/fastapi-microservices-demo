import pika
from pika.exchange_type import ExchangeType


class RabbitMQClient:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.url = None
        self.exchange_name = None

    def setup(self, url, exchange_name):

        self.url = url
        self.exchange_name = exchange_name

    def connect(self):

        if self.connection and self.connection.is_open:
            return

        self.connection = pika.BlockingConnection(pika.URLParameters(self.url))
        self.channel = self.connection.channel()

        # Declare an exchange. The type is direct, which routes the message
        # to multiple queues based on the queue bindings.
        # Messages in each queue will be consumed by a TYPE of consumer.
        # channel.queue_declare(queue=queue_name)
        self.channel.exchange_declare(
            exchange=self.exchange_name,
            exchange_type=ExchangeType.direct,
        )

    def publish(self, routing_key, message):
        # self.connect()
        # self.channel.basic_publish(
        #     exchange=self.exchange_name,
        #     routing_key=routing_key,
        #     body=message,
        # )

        try:
            self.connect()

            self.channel.basic_publish(
                exchange=self.exchange_name,
                routing_key=routing_key,
                body=message,
            )
        except pika.exceptions.AMQPConnectionError:
            self.close()
        finally:
            self.close()

    def listen(self, routing_key, on_msg_received_handler):
        self.connect()

        # Each consumer will still need its own dedicated queue.
        # But we don't specify a queue name. Instead we provide an empty string
        # which will let the server decide on a name dynamically.
        # exclusive=True means the queue can be deleted with the consumer is closed.
        queue = self.channel.queue_declare(queue="", exclusive=True, durable=True)
        self.channel.queue_bind(
            exchange=self.exchange_name,
            queue=queue.method.queue,
            routing_key=routing_key,
        )

        self.channel.basic_consume(
            queue=queue.method.queue,
            auto_ack=False,
            on_message_callback=on_msg_received_handler,
        )

        self.channel.start_consuming()

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
            # self.channel.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def check_conn(self):

        if self.connection and self.connection.is_open:
            return True

        try:
            connection = pika.BlockingConnection(pika.URLParameters(self.url))
            connection.close()
            return True
        except pika.exceptions.AMQPConnectionError:
            return False


rmq_client = RabbitMQClient()


async def get_rmq():
    return rmq_client
