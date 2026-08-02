from app.application.ports.strategy_port import StrategyPort

class MultiSMAsMomentumStrategy(StrategyPort):
    def evaluate(self, trend_candles, context_candles, entry_candles):

        return None
    
class RSICrossSMATrendStrategy(StrategyPort):
    def evaluate(self, trend_candles, context_candles, entry_candles):
        
        return None
