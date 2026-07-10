from abc import ABC
from abc import abstractmethod

class NotificationProvider(ABC):
    @abstractmethod
    def send(
        self,
        token: str,
        chat_id: str,
        message: str,
    ):
        pass
