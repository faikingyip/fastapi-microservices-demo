import time

import pika

from src.common.ctx.rmq_client import RMQClient


class Listener:
    """Data class"""

    def __init__(
        self,
        routing_key,
        on_msg_received_handler,
    ):
        self.routing_key = routing_key
        self.on_msg_received_handler = on_msg_received_handler


class RMQListenerClient(RMQClient):
    """A client specifically for listening or
    consuming messages from RabbitMQ."""

    def __init__(self):
        super().__init__()
        self.listener_routing_key_map = {}

    def on_msg_received_handler(self, channel, method, properties, body):
        """The generic handler for messages received. The routing
        key is then assessed to determine which specific registered
        listener should be used to handle the event."""
        handler = self.listener_routing_key_map[method.routing_key]
        handler(channel, method, properties, body)

    def set_listeners(self, listeners: list[Listener]):
        """The listeners to register, along with its routing key."""
        for listener in listeners:
            self.listener_routing_key_map[listener.routing_key] = (
                listener.on_msg_received_handler
            )

    def listen(self):
        while True:
            try:
                self.connect()

                # Each consumer will still need its own dedicated queue.
                # But we don't specify a queue name. Instead we provide an empty string
                # which will let the server decide on a name dynamically.
                # exclusive=True means the queue can be deleted with the consumer is closed.
                queue = self.channel.queue_declare(
                    queue="", exclusive=True, durable=True
                )

                for routing_key in self.listener_routing_key_map:
                    self.channel.queue_bind(
                        exchange=self.exchange_name,
                        queue=queue.method.queue,
                        routing_key=routing_key,
                    )

                self.channel.basic_consume(
                    queue=queue.method.queue,
                    auto_ack=False,
                    on_message_callback=self.on_msg_received_handler,
                )

                self.channel.start_consuming()
            except pika.exceptions.AMQPConnectionError:
                time.sleep(3)
            except pika.exceptions.ChannelWrongStateError:
                time.sleep(3)

    async def get_rmq_listener_client(self):
        return self
