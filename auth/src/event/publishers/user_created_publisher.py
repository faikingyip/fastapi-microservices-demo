from src.common.rabbit_mq import RabbitMQClient
from src.constants.event_subject import EventSubjects


class UserCreatedPublisher:
    def __init__(self, client: RabbitMQClient):
        self.client: RabbitMQClient = client
        self.subject = EventSubjects.USER_CREATED

    def publish(self, msg):
        print("PUBLISHING")
        self.client.publish(self.subject, msg)
