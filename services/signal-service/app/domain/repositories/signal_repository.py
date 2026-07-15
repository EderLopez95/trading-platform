from abc import ABC, abstractmethod
from app.domain.entities.signal import Signal

class SignalRepository(ABC):
    @abstractmethod
    def create(self, signal: Signal) -> Signal:
        pass

    @abstractmethod
    def exists(self, user_id: str, dedup_key: str, candle_time):
        pass

    @abstractmethod
    def get_by_user(self, user_id: str) -> list[Signal]:
        pass
