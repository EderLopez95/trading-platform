from app.domain.enums.enums import SignalType
from app.domain.entities.strategy_result import StrategyResult
from app.domain.indicators.rsi_cross import RSICross
import pandas as pd

class MultiSMAsMomentumStrategy:
    def __init__(self):
        self.rsi_cross = RSICross()

    def evaluate(self, candles):
        closes = [
            candle.close
            for candle in candles
        ]
        close_series = pd.Series(closes)

        if len(closes) < 100:

            return StrategyResult(
                signal=SignalType.NONE,
                reason="Not enough candles",
            )

        # calculate SMAs (averages, last value)
        sma20 = close_series.rolling(20).mean()
        sma40 = close_series.rolling(40).mean()
        sma100 = close_series.rolling(100).mean()
        sma20_v = sma20.iloc[-1]
        sma40_v = sma40.iloc[-1]
        sma100_v = sma100.iloc[-1]

        if pd.isna(sma100_v): # in case of invalid data
            
            return StrategyResult(
                signal=SignalType.NONE,
                reason="Invalid SMA values",
            )

        # determine trend based on SMA order
        bullish_trend = (
            sma20_v > sma40_v
            and
            sma40_v > sma100_v
        )
        bearish_trend = (
            sma20_v < sma40_v
            and
            sma40_v < sma100_v
        )

        # trend strength, avoid laterality
        min_distance = 0.002
        distance_20_40 = abs(sma20_v - sma40_v) / sma40_v
        distance_40_100 = abs(sma40_v - sma100_v) / sma100_v
        trend_strength = (
            distance_20_40 > min_distance
            and
            distance_40_100 > min_distance
        )

        # trend slope
        sma20_slope = sma20_v - sma20.iloc[-4]
        trend_direction_ok = abs(sma20_slope) > 0

        # calculate RSI entry
        rsi = self.rsi_cross.calculate_rsi(close_series, 14)
        rsi_ma = rsi.rolling(14).mean()
        bullish_cross = self.rsi_cross.crossover(rsi, rsi_ma)
        bearish_cross = self.rsi_cross.crossunder(rsi, rsi_ma)
        
        volume_avg = pd.Series([candle.volume for candle in candles]).rolling(20).mean()
        if pd.isna(volume_avg.iloc[-1]): # in case of invalid data

            return StrategyResult(
                signal=SignalType.NONE,
                reason="Invalid volume values",
            )
        
        volume_v = candles[-1].volume
        volume_avg_v = volume_avg.iloc[-1]
        volume_ok = volume_v > (volume_avg_v * 1.2) # considerable movement, increase it to filter more deeply

        if bullish_trend and bullish_cross and trend_strength and trend_direction_ok and volume_ok:

            return StrategyResult(signal=SignalType.BUY)

        if bearish_trend and bearish_cross and trend_strength and trend_direction_ok and volume_ok:

            return StrategyResult(signal=SignalType.SELL)

        return StrategyResult(signal=SignalType.NONE)
