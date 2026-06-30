from abc import ABC
from abc import abstractmethod

class MarketDataProvider(ABC):
    @abstractmethod
    def get_candles(
        self,
        symbol: str,
        timeframe: str,
        count: int,
    ):
        pass
