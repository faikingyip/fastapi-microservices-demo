from src.common.rabbit_mq import RabbitMQClient


class UserCreatedPublisher:
    def __init__(self, client: RabbitMQClient):
        self.client: RabbitMQClient = client
        self.subject = "user:created"

    def publish(self, msg):
        self.client.publish(self.subject, msg)
