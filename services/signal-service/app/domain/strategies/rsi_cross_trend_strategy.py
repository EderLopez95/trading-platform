from app.domain.enums.enums import SignalType
from app.domain.indicators.rsi_cross import RSICross
from app.domain.entities.strategy_result import StrategyResult
import pandas as pd

class RSICrossTrendStrategy:
    def __init__(self):
        self.rsi_cross = RSICross()

    def evaluate(self, candles):
        closes = [
            candle.close
            for candle in candles
        ]
        close_series = pd.Series(closes)

        if len(closes) < 50:

            return StrategyResult(
                signal=SignalType.NONE,
                reason="Not enough candles",
            )

        # calculate RSI
        rsi = self.rsi_cross.calculate_rsi(close_series, 14)
        rsi_ma = rsi.rolling(14).mean()
        bullish_cross = self.rsi_cross.crossover(rsi, rsi_ma)
        bearish_cross = self.rsi_cross.crossunder(rsi, rsi_ma)

        if bullish_cross:
            return StrategyResult(signal=SignalType.BUY)

        if bearish_cross:
            return StrategyResult(signal=SignalType.SELL)

        return StrategyResult(signal=SignalType.NONE)
