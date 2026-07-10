from app.application.ports.market_data_port import MarketDataPort
from app.infrastructure.grpc.clients.market_data_client import MarketDataClient

class MarketDataAdapter(MarketDataPort):
    def __init__(self):
        self.client = (MarketDataClient())

    def get_candles(
        self,
        symbol: str,
        timeframe: str,
        count: int,
    ):
        
        return self.client.get_candles(
            symbol,
            timeframe,
            count,
        )
