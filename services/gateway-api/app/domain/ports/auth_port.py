from abc import ABC, abstractmethod

class AuthPort(ABC):
    @abstractmethod
    def register(self, email: str, password: str):
        pass

    @abstractmethod
    def login(self, email: str, password: str):
        pass

    @abstractmethod
    def validate(self, token: str):
        pass

    @abstractmethod
    def update_telegram(self, user_id: str, token: str, chat_id: str):
        pass

    @abstractmethod
    def get_user(self, user_id: str):
        pass
