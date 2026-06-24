from abc import ABC, abstractmethod

class MarketDataPort(ABC):
    @abstractmethod
    def get_candles(
        self,
        symbol: str,
        timeframe: str,
        count: int,
    ):
        pass
