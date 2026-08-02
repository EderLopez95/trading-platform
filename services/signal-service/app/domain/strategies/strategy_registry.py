from app.domain.strategies.multi_smas_momentum_strategy import MultiSMAsMomentumStrategy
from app.domain.strategies.rsi_cross_sma_trend_strategy import RSICrossSMATrendStrategy

class StrategyRegistry:
    def __init__(self):
        self._strategies = {
            "multi_smas_momentum": MultiSMAsMomentumStrategy(),
            "rsi_cross_sma_trend": RSICrossSMATrendStrategy(),
        }

    def get(self, strategy_name: str):
        
        return self._strategies.get(strategy_name)

    def get_all(self):

        return {k: self._strategies[k] for k in sorted(self._strategies)}
        
    def get_names(self):
        
        return sorted(self._strategies.keys())
