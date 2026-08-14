from app.domain.enums.enums import SignalType
from app.domain.entities.strategy_result import StrategyResult
from app.domain.indicators.rsi_cross import RSICross
import pandas as pd

class StockMomentumStrategy:
    def __init__(
        self,
        sma_fast=9,
        sma_mid=21,
        sma_slow=50,
        context_sma_fast=20,
        context_sma_slow=50,
        rsi_period=14,
        min_sma_distance=0.0015,
        volume_multiplier=1.2,   # breakout volume must exceed the recent average to confirm momentum
        volume_lookback=20,
        cross_window=3,
    ):
        self.rsi_cross = RSICross()
        self.sma_fast = sma_fast
        self.sma_mid = sma_mid
        self.sma_slow = sma_slow
        self.context_sma_fast = context_sma_fast
        self.context_sma_slow = context_sma_slow
        self.rsi_period = rsi_period
        self.min_sma_distance = min_sma_distance
        self.volume_multiplier = volume_multiplier
        self.volume_lookback = volume_lookback
        self.cross_window = cross_window

    def evaluate(self, trend_candles, context_candles, entry_candles):

        entry_min = max(self.rsi_period * 2, self.volume_lookback) + self.cross_window

        if not trend_candles or len(trend_candles) < self.sma_slow:

            return StrategyResult(
                signal=SignalType.NONE,
                reason="Not enough candles for trend timeframe",
            )

        if context_candles and len(context_candles) < self.context_sma_slow: # optional

            return StrategyResult(
                signal=SignalType.NONE,
                reason="Not enough candles for context timeframe",
            )

        if not entry_candles or len(entry_candles) < entry_min:

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

        sma_fast = trend_close_series.rolling(self.sma_fast).mean()
        sma_mid = trend_close_series.rolling(self.sma_mid).mean()
        sma_slow = trend_close_series.rolling(self.sma_slow).mean()
        sma_fast_v = sma_fast.iloc[-1]
        sma_mid_v = sma_mid.iloc[-1]
        sma_slow_v = sma_slow.iloc[-1]

        if pd.isna(sma_slow_v):
            
            return StrategyResult(
                signal=SignalType.NONE,
                reason="Invalid trend SMA values",
            )
        
        trend_bullish = (
            sma_fast_v > sma_mid_v
            and sma_mid_v > sma_slow_v
        )
        trend_bearish = (
            sma_fast_v < sma_mid_v
            and sma_mid_v < sma_slow_v
        )

        distance_fast_mid = abs(sma_fast_v - sma_mid_v) / sma_mid_v
        distance_mid_slow = abs(sma_mid_v - sma_slow_v) / sma_slow_v
        trend_strength = (
            distance_fast_mid > self.min_sma_distance
            and distance_mid_slow > self.min_sma_distance
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

        entry_rsi = self.rsi_cross.calculate_rsi_ema(entry_close_series, self.rsi_period)
        entry_rsi_ma = entry_rsi.ewm(span=self.rsi_period, adjust=False, min_periods=1).mean()

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

        volume_avg = pd.Series([candle.volume for candle in entry_candles]).rolling(self.volume_lookback).mean()
        
        if pd.isna(volume_avg.iloc[-1]):

            return StrategyResult(
                signal=SignalType.NONE,
                reason="Invalid entry volume values",
            )
        
        volume_avg_v = volume_avg.iloc[-1]
        recent_volume = max(candle.volume for candle in entry_candles[-self.cross_window:]) # volume on the crossover candle, not necessarily the last one
        entry_volume_ok = recent_volume >= (volume_avg_v * self.volume_multiplier)

        # CONTEXT TIMEFRAME
        
        context_bullish = True
        context_bearish = True

        if context_candles:

            context_closes = [
                candle.close
                for candle in context_candles
            ]
            context_close_series = pd.Series(context_closes)

            context_sma_fast = context_close_series.rolling(self.context_sma_fast).mean()
            context_sma_slow = context_close_series.rolling(self.context_sma_slow).mean()
            context_sma_fast_v = context_sma_fast.iloc[-1]
            context_sma_slow_v = context_sma_slow.iloc[-1]

            if pd.isna(context_sma_slow_v):

                return StrategyResult(
                    signal=SignalType.NONE,
                    reason="Invalid context SMA values",
                )

            context_bullish = context_sma_fast_v > context_sma_slow_v
            context_bearish = context_sma_fast_v < context_sma_slow_v

        # VALIDATE CONDITIONS

        if (
            trend_bullish
            and trend_strength
            and context_bullish
            and entry_bullish_cross
            and entry_volume_ok
        ):

            return StrategyResult(signal=SignalType.BUY)

        if (
            trend_bearish
            and trend_strength
            and context_bearish
            and entry_bearish_cross
            and entry_volume_ok
        ):

            return StrategyResult(signal=SignalType.SELL)

        return StrategyResult(signal=SignalType.NONE)
