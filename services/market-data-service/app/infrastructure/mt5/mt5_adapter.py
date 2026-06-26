from app.domain.entities.candle import (
    Candle,
)

from app.domain.ports.market_data_provider import (
    MarketDataProvider,
)


class MT5Adapter(
    MarketDataProvider
):

    def get_candles(
        self,
        symbol: str,
        timeframe: str,
        count: int,
    ):

        return []