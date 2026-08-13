from app.domain.strategies.stock_momentum_strategy import StockMomentumStrategy
from app.domain.strategies.forex_momentum_strategy import ForexMomentumStrategy

class StrategyRegistry:
    def __init__(self):
        self._strategies = {
            "stock_momentum": StockMomentumStrategy(),
            "forex_momentum": ForexMomentumStrategy(),
        }

    def get(self, strategy_name: str):
        
        return self._strategies.get(strategy_name)

    def get_all(self):

        return {k: self._strategies[k] for k in sorted(self._strategies)}
        
    def get_names(self):
        
        return sorted(self._strategies.keys())
