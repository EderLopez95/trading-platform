from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str):
        pass

    @abstractmethod
    def create(self, email: str, password_hash: str):
        pass
