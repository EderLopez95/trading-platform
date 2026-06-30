class MarketDataService:
    def __init__(self, provider):
        self.provider = provider

    def get_candles(
        self,
        symbol: str,
        timeframe: str,
        count: int,
    ):
        
        return self.provider.get_candles(symbol, timeframe, count)
