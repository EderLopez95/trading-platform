from app.infrastructure.mt5.mt5_adapter import MT5Adapter

class MarketDataService:
    def __init__(self, provider: MT5Adapter):
        self.provider = provider

    def get_candles(
        self,
        symbol: str,
        timeframe: str,
        count: int,
    ):
        
        return self.provider.get_candles(symbol, timeframe, count)
