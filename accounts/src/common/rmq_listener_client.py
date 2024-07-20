import time

import pika
from pika.exchange_type import ExchangeType

from src.common.rmq_client import RMQClient


class Listener:
    def __init__(
        self,
        routing_key,
        on_msg_received_handler,
    ):
        self.routing_key = routing_key
        self.on_msg_received_handler = on_msg_received_handler


class RMQListenerClient(RMQClient):
    def __init__(self):
        super().__init__()
        self.listener_routing_key_map = {}
        # self.listeners: list[Listener] = []

    def on_msg_received_handler(self, channel, method, properties, body):
        handler = self.listener_routing_key_map[method.routing_key]
        handler(channel, method, properties, body)

    def reconnect(self):
        try:
            self.connect()
        except Exception as e:
            print(f"Failed to reconnect: {e}")
            time.sleep(5)  # Wait before trying to reconnect

    def set_listeners(self, listeners: list[Listener]):
        # self.listeners = listeners

        for listener in listeners:
            self.listener_routing_key_map[listener.routing_key] = (
                listener.on_msg_received_handler
            )

    # def listen(self, routing_key, on_msg_received_handler):
    def listen(self):
        self.connect()

        # Each consumer will still need its own dedicated queue.
        # But we don't specify a queue name. Instead we provide an empty string
        # which will let the server decide on a name dynamically.
        # exclusive=True means the queue can be deleted with the consumer is closed.
        queue = self.channel.queue_declare(queue="", exclusive=True, durable=True)

        for routing_key in self.listener_routing_key_map:
            self.channel.queue_bind(
                exchange=self.exchange_name,
                queue=queue.method.queue,
                routing_key=routing_key,
            )

        while True:
            try:
                self.channel.basic_consume(
                    queue=queue.method.queue,
                    auto_ack=False,
                    on_message_callback=self.on_msg_received_handler,
                )

                self.channel.start_consuming()
            except pika.exceptions.AMQPConnectionError:
                time.sleep(1)
                self.reconnect()

    def close(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
            # self.channel.close()

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    async def get_rmq_listener_client(self):
        return self