from src.common.rabbit_mq import RabbitMQClient
from src.constants.event_subject import EventSubjects


class TransactionCreatedPublisher:
    def __init__(self, client: RabbitMQClient):
        self.client: RabbitMQClient = client
        self.subject = EventSubjects.TRANSACTION_CREATED

    def publish(self, msg):
        self.client.publish(self.subject, msg)
