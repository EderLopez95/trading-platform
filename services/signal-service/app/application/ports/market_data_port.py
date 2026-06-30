from abc import ABC
from abc import abstractmethod

class MarketDataPort(ABC):
    @abstractmethod
    def get_candles(
        self,
        symbol: str,
        timeframe: str,
        count: int,
    ):
        pass
