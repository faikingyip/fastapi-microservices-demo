import abc


class AbstractDbManager(abc.ABC):

    @abc.abstractmethod
    def check_conn(self):
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_session(self):
        raise NotImplementedError()


class AbstractMsgPublisherClient(abc.ABC):

    @abc.abstractmethod
    def publish(self, routing_key, message):
        raise NotImplementedError()

    @abc.abstractmethod
    def __enter__(self):
        raise NotImplementedError()

    @abc.abstractmethod
    def __exit__(self, exc_type, exc_val, exc_tb):
        raise NotImplementedError()

    @abc.abstractmethod
    def check_conn(self):
        raise NotImplementedError()
