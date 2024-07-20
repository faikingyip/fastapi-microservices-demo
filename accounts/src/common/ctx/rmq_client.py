import socket
from abc import ABC

import pika
from pika.exchange_type import ExchangeType


class RMQClient(ABC):
    """Abstract class to hold all the common methods
    related to connection to the RabbitMQ server."""

    def __init__(self):
        self.connection = None
        self.channel = None
        self.url = None
        self.exchange_name = None

    def setup(
        self,
        rmq_host,
        rmq_port,
        rmq_user,
        rmq_pass,
        exchange_name,
    ):
        self.url = f"amqp://{rmq_user}:{rmq_pass}@{rmq_host}:{rmq_port}"
        self.exchange_name = exchange_name

    def connect(self):
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

    def check_conn(self):
        """Checks the connection to the RabbitMQ server."""
        try:
            connection = pika.BlockingConnection(pika.URLParameters(self.url))
            connection.close()
            return True
        except pika.exceptions.AMQPConnectionError:
            return False
        except pika.exceptions.ChannelWrongStateError:
            return False
        except socket.gaierror:
            return False

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
        if self.channel and self.channel.is_open:
            self.channel.close()
