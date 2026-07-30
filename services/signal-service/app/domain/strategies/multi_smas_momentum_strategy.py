from app.domain.enums.enums import SignalType
from app.domain.entities.strategy_result import StrategyResult
from app.domain.indicators.rsi_cross import RSICross
import pandas as pd

class MultiSMAsMomentumStrategy:
    def __init__(
        self,
        min_sma_distance=0.002,
        volume_multiplier=0.7,
        min_slope_strength=0.001
    ):
        self.rsi_cross = RSICross()
        self.min_sma_distance = min_sma_distance
        self.volume_multiplier = volume_multiplier
        self.min_slope_strength = min_slope_strength

    def evaluate(self, trend_candles, context_candles, entry_candles):
        
        if len(trend_candles) < 100:

            return StrategyResult(
                signal=SignalType.NONE,
                reason="Not enough candles for trend timeframe",
            )

        if len(entry_candles) < 20:
        
            return StrategyResult(
                signal=SignalType.NONE,
                reason="Not enough candles for entry timeframe",
            )

        trend_closes = [
            candle.close
            for candle in trend_candles
        ]
        trend_close_series = pd.Series(trend_closes)

        entry_closes = [
            candle.close
            for candle in entry_candles
        ]
        entry_close_series = pd.Series(entry_closes)

        # calculate SMAs (averages, last value)
        sma20 = trend_close_series.rolling(20).mean()
        sma40 = trend_close_series.rolling(40).mean()
        sma100 = trend_close_series.rolling(100).mean()
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
            and sma40_v > sma100_v
        )
        bearish_trend = (
            sma20_v < sma40_v
            and sma40_v < sma100_v
        )

        # trend strength, avoid laterality
        distance_20_40 = abs(sma20_v - sma40_v) / sma40_v
        distance_40_100 = abs(sma40_v - sma100_v) / sma100_v
        trend_strength = (
            distance_20_40 > self.min_sma_distance
            and distance_40_100 > self.min_sma_distance
        )

        # trend slope
        sma20_slope = sma20_v - sma20.iloc[-4]
        trend_direction_ok = abs(sma20_slope) > (sma20_v * self.min_slope_strength)

        # calculate RSI entry
        entry_rsi = self.rsi_cross.calculate_rsi(entry_close_series, 14)
        entry_rsi_ma = entry_rsi.rolling(14).mean()
        bullish_cross = self.rsi_cross.crossover(entry_rsi, entry_rsi_ma)
        bearish_cross = self.rsi_cross.crossunder(entry_rsi, entry_rsi_ma)

        # calculate volume average and check if current volume is low
        volume_avg = pd.Series([candle.volume for candle in entry_candles]).rolling(20).mean()
        if pd.isna(volume_avg.iloc[-1]): # in case of invalid data

            return StrategyResult(
                signal=SignalType.NONE,
                reason="Invalid volume values",
            )
        
        volume_v = entry_candles[-1].volume
        volume_avg_v = volume_avg.iloc[-1]
        volume_low = volume_v < (volume_avg_v * self.volume_multiplier)

        if (
            bullish_trend
            and bullish_cross
            and trend_strength
            and trend_direction_ok
            and not volume_low
        ):

            return StrategyResult(signal=SignalType.BUY)

        if (
            bearish_trend
            and bearish_cross
            and trend_strength
            and trend_direction_ok
            and not volume_low
        ):

            return StrategyResult(signal=SignalType.SELL)

        return StrategyResult(signal=SignalType.NONE)
