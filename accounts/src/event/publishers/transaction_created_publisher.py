from src.common.rmq.rmq_publisher_client import RMQPublisherClient
from src.constants.event_subject import EventSubjects


class AccountUpdatedPublisher:
    def __init__(self, client: RMQPublisherClient):
        self.client: RMQPublisherClient = client
        self.subject = EventSubjects.ACCOUNT_UPDATED

    def publish(self, msg):
        with self.client:
            self.client.publish(self.subject, msg)
