from app.domain.strategies.multi_smas_momentum_strategy import MultiSMAsMomentumStrategy
from app.domain.strategies.rsi_cross_trend_strategy import RSICrossTrendStrategy

class StrategyRegistry:
    def __init__(self):
        self._strategies = {
            "multi_smas_momentum": MultiSMAsMomentumStrategy(),
            "rsi_cross_trend": RSICrossTrendStrategy(),
        }

    def get(self, strategy_name: str):
        
        return self._strategies.get(strategy_name)

    def get_all(self):
        
        return self._strategies

    def get_names(self):
        
        return list(self._strategies.keys())
