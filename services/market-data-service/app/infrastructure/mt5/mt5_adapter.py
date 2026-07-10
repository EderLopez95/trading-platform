from datetime import datetime
from typing import List
import MetaTrader5 as mt5
from app.domain.entities.candle import Candle
from app.domain.ports.market_data_provider import MarketDataProvider
from app.infrastructure.mt5.timeframe_mapper import TIMEFRAME_MAP
from app.domain.exceptions.exceptions import TimeframeNotSupportedException, SymbolNotFoundException, RuntimeException

class MT5Adapter(MarketDataProvider):
    def __init__(self):
        
        if not mt5.initialize():
            raise RuntimeError(f"MT5 initialize failed: {mt5.last_error()}")

    def get_candles(
        self,
        symbol: str,
        timeframe: str,
        count: int,
    ) -> List[Candle]:
        mt5_timeframe = TIMEFRAME_MAP.get(timeframe)

        if not mt5_timeframe:
            raise TimeframeNotSupportedException(timeframe)

        symbol_info = mt5.symbol_info(symbol)

        if symbol_info is None:
            raise SymbolNotFoundException(symbol)

        if not symbol_info.visible:
            if not mt5.symbol_select(symbol, True):
                raise RuntimeException(f"Unable to select symbol: {symbol}")

        rates = mt5.copy_rates_from_pos(
            symbol,
            mt5_timeframe,
            0,
            count,
        )

        if rates is None:
            raise RuntimeException(f"Unable to retrieve candles for {symbol}: {mt5.last_error()}")

        candles: list[Candle] = []

        for rate in rates:
            candles.append(
                Candle(
                    timestamp=datetime.fromtimestamp(rate["time"]),
                    open=float(rate["open"]),
                    high=float(rate["high"]),
                    low=float(rate["low"]),
                    close=float(rate["close"]),
                    volume=float(rate["tick_volume"]),
                )
            )

        return candles

    def shutdown(self):
        mt5.shutdown()
