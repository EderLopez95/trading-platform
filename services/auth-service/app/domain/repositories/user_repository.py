from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str):
        pass

    @abstractmethod
    def create(self, email: str, password_hash: str):
        pass

    @abstractmethod
    def get_by_id(self, user_id: str):
        pass

    @abstractmethod
    def update_telegram(self, user, token: str, chat_id: str):
        pass
