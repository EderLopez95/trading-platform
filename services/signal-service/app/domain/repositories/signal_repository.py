from abc import ABC, abstractmethod
from app.domain.entities.signal import Signal

class SignalRepository(ABC):
    @abstractmethod
    def create(self, signal: Signal) -> Signal:
        pass

    @abstractmethod
    def get_by_user(self, user_id: str) -> list[Signal]:
        pass
