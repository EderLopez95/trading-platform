from datetime import datetime, timezone
from app.application.ports.market_data_port import MarketDataPort
from app.domain.entities.candle import Candle

class MockMarketDataAdapter(MarketDataPort):
    def get_candles(
        self,
        symbol: str,
        timeframe: str,
        count: int,
    ):
        candles = []

        for i in range(count):
            candles.append(
                Candle(
                    timestamp=datetime.now(timezone.utc),
                    open=100,
                    high=105,
                    low=99,
                    close=104,
                    volume=1000,
                )
            )

        return candles
