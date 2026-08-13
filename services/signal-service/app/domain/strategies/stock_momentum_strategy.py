from app.domain.enums.enums import SignalType
from app.domain.entities.strategy_result import StrategyResult
from app.domain.indicators.rsi_cross import RSICross
import pandas as pd

class StockMomentumStrategy:
    def __init__(
        self,
        min_sma_distance=0.0015,
        volume_multiplier=0.7,
        cross_window=3,
    ):
        self.rsi_cross = RSICross()
        self.min_sma_distance = min_sma_distance
        self.volume_multiplier = volume_multiplier
        self.cross_window = cross_window

    def evaluate(self, trend_candles, context_candles, entry_candles):
        
        if not trend_candles or len(trend_candles) < 90:

            return StrategyResult(
                signal=SignalType.NONE,
                reason="Not enough candles for trend timeframe",
            )
        
        if context_candles and len(context_candles) < 90: # optional
        
            return StrategyResult(
                signal=SignalType.NONE,
                reason="Not enough candles for context timeframe",
            )

        if not entry_candles or len(entry_candles) < 40:
        
            return StrategyResult(
                signal=SignalType.NONE,
                reason="Not enough candles for entry timeframe",
            )

        # TREND TIMEFRAME

        trend_closes = [
            candle.close
            for candle in trend_candles
        ]
        trend_close_series = pd.Series(trend_closes)

        sma20 = trend_close_series.rolling(20).mean()
        sma40 = trend_close_series.rolling(40).mean()
        sma100 = trend_close_series.rolling(100).mean()
        sma20_v = sma20.iloc[-1]
        sma40_v = sma40.iloc[-1]
        sma100_v = sma100.iloc[-1]

        if pd.isna(sma100_v) or pd.isna(sma20.iloc[-4]):
            
            return StrategyResult(
                signal=SignalType.NONE,
                reason="Invalid trend SMA values",
            )
        
        trend_bullish = (
            sma20_v > sma40_v
            and sma40_v > sma100_v
        )
        trend_bearish = (
            sma20_v < sma40_v
            and sma40_v < sma100_v
        )

        distance_20_40 = abs(sma20_v - sma40_v) / sma40_v
        distance_40_100 = abs(sma40_v - sma100_v) / sma100_v
        trend_strength = (
            distance_20_40 > self.min_sma_distance
            and distance_40_100 > self.min_sma_distance
        )

        if (
            (not trend_bullish and not trend_bearish)
            or not trend_strength
        ):

            return StrategyResult(signal=SignalType.NONE)
        
        # ENTRY TIMEFRAME

        entry_closes = [
            candle.close
            for candle in entry_candles
        ]
        entry_close_series = pd.Series(entry_closes)

        entry_rsi = self.rsi_cross.calculate_rsi_ema(entry_close_series, 14)
        entry_rsi_ma = entry_rsi.ewm(span=14, adjust=False, min_periods=1).mean()

        if (
            pd.isna(entry_rsi.iloc[-1]) or pd.isna(entry_rsi.iloc[-2])
            or pd.isna(entry_rsi_ma.iloc[-1]) or pd.isna(entry_rsi_ma.iloc[-2])
        ):
            
            return StrategyResult(
                signal=SignalType.NONE,
                reason="Calculated entry RSI indicators contain NaN at evaluation indices",
            )

        entry_bullish_cross = self.rsi_cross.crossover_within(entry_rsi, entry_rsi_ma, self.cross_window)
        entry_bearish_cross = self.rsi_cross.crossunder_within(entry_rsi, entry_rsi_ma, self.cross_window)

        volume_avg = pd.Series([candle.volume for candle in entry_candles]).rolling(20).mean()
        
        if pd.isna(volume_avg.iloc[-1]):

            return StrategyResult(
                signal=SignalType.NONE,
                reason="Invalid entry volume values",
            )
        
        volume_v = entry_candles[-1].volume
        volume_avg_v = volume_avg.iloc[-1]
        entry_volume_low = volume_v < (volume_avg_v * self.volume_multiplier)

        # CONTEXT TIMEFRAME
        
        context_bullish = True
        context_bearish = True

        if context_candles:

            context_closes = [
                candle.close
                for candle in context_candles
            ]
            context_close_series = pd.Series(context_closes)

            context_sma20 = context_close_series.rolling(20).mean()
            context_sma40 = context_close_series.rolling(40).mean()
            context_sma20_v = context_sma20.iloc[-1]
            context_sma40_v = context_sma40.iloc[-1]

            if pd.isna(context_sma40_v):

                return StrategyResult(
                    signal=SignalType.NONE,
                    reason="Invalid context SMA values",
                )

            context_bullish = context_sma20_v > context_sma40_v
            context_bearish = context_sma20_v < context_sma40_v

        # VALIDATE CONDITIONS

        if (
            trend_bullish
            and trend_strength
            and context_bullish
            and entry_bullish_cross
            and not entry_volume_low
        ):

            return StrategyResult(signal=SignalType.BUY)

        if (
            trend_bearish
            and trend_strength
            and context_bearish
            and entry_bearish_cross
            and not entry_volume_low
        ):

            return StrategyResult(signal=SignalType.SELL)

        return StrategyResult(signal=SignalType.NONE)
