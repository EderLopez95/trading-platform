from abc import ABC
from abc import abstractmethod

class StrategyPort(ABC):
    @abstractmethod
    def evaluate(self, candles):
        pass
