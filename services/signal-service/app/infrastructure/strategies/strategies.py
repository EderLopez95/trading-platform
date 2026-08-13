from app.application.ports.strategy_port import StrategyPort

class StockMomentumStrategy(StrategyPort):
    def evaluate(self, trend_candles, context_candles, entry_candles):

        return None
    
class ForexMomentumStrategy(StrategyPort):
    def evaluate(self, trend_candles, context_candles, entry_candles):
        
        return None
