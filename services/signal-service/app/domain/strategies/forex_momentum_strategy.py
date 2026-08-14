from app.domain.enums.enums import SignalType
from app.domain.entities.strategy_result import StrategyResult
from app.domain.indicators.macd import MACD
import pandas as pd

class ForexMomentumStrategy:
    def __init__(
        self,
        ema_fast=9,
        ema_mid=21,
        ema_slow=50,
        context_ema=21,         # H1 directional bias only; EMA50 on H1 was too slow for a 2-3h day trade
        breakout_lookback=10,
        min_body_ratio=0.4,
        pip_size=0.0001,        # EURUSD / non-JPY 5-digit pairs; JPY pairs would use 0.01
        min_macd_pips=0.2,      # MACD histogram must clear this many pips to confirm real momentum (M5 histograms are small)
        volume_multiplier=1.0,  # breakout tick volume at/above recent average (tick volume is a valid activity proxy on forex)
        volume_lookback=20,
        trigger_window=3,       # breakout + momentum may build within the last N entry candles (not one exact bar)
    ):
        self.macd = MACD()
        self.ema_fast = ema_fast
        self.ema_mid = ema_mid
        self.ema_slow = ema_slow
        self.context_ema = context_ema
        self.breakout_lookback = breakout_lookback
        self.min_body_ratio = min_body_ratio
        self.pip_size = pip_size
        self.min_macd_pips = min_macd_pips
        self.volume_multiplier = volume_multiplier
        self.volume_lookback = volume_lookback
        self.trigger_window = trigger_window

    def evaluate(self, trend_candles, context_candles, entry_candles):
        trend_min = self.ema_slow
        context_min = self.context_ema
        entry_min = self.macd.slow_period + self.macd.signal_period

        if not trend_candles or len(trend_candles) < trend_min:

            return StrategyResult(
                signal=SignalType.NONE,
                reason="Not enough candles for trend timeframe",
            )

        if context_candles and len(context_candles) < context_min: # optional

            return StrategyResult(
                signal=SignalType.NONE,
                reason="Not enough candles for context timeframe",
            )

        if not entry_candles or len(entry_candles) < max(entry_min, self.breakout_lookback + self.trigger_window, self.volume_lookback):

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

        ema_fast = trend_close_series.ewm(span=self.ema_fast, adjust=False, min_periods=self.ema_fast).mean()
        ema_mid = trend_close_series.ewm(span=self.ema_mid, adjust=False, min_periods=self.ema_mid).mean()
        ema_slow = trend_close_series.ewm(span=self.ema_slow, adjust=False, min_periods=self.ema_slow).mean()
        ema_fast_v = ema_fast.iloc[-1]
        ema_mid_v = ema_mid.iloc[-1]
        ema_slow_v = ema_slow.iloc[-1]

        if pd.isna(ema_slow_v):

            return StrategyResult(
                signal=SignalType.NONE,
                reason="Invalid trend EMA values",
            )

        trend_bullish = (
            ema_fast_v > ema_mid_v
            and ema_mid_v > ema_slow_v
        )
        trend_bearish = (
            ema_fast_v < ema_mid_v
            and ema_mid_v < ema_slow_v
        )

        if not trend_bullish and not trend_bearish:

            return StrategyResult(signal=SignalType.NONE)

        # ENTRY TIMEFRAME

        entry_closes = [
            candle.close
            for candle in entry_candles
        ]
        entry_close_series = pd.Series(entry_closes)

        macd_line, signal_line, histogram = self.macd.calculate(entry_close_series)

        if (
            pd.isna(macd_line.iloc[-1]) or pd.isna(signal_line.iloc[-1])
            or pd.isna(histogram.iloc[-1]) or pd.isna(histogram.iloc[-2])
        ):

            return StrategyResult(
                signal=SignalType.NONE,
                reason="Calculated entry MACD indicators contain NaN at evaluation indices",
            )

        macd_v = float(macd_line.iloc[-1])
        signal_v = float(signal_line.iloc[-1])

        macd_threshold = self.min_macd_pips * self.pip_size

        recent_hist = histogram.iloc[-self.trigger_window:] # momentum can build anywhere within the trigger window
        hist_max = float(recent_hist.max())
        hist_min = float(recent_hist.min())

        momentum_bullish = macd_v > signal_v and hist_max > macd_threshold
        momentum_bearish = macd_v < signal_v and hist_min < -macd_threshold

        prior = entry_candles[-(self.breakout_lookback + self.trigger_window):-self.trigger_window] # range before the trigger window
        recent_high = max(candle.high for candle in prior)
        recent_low = min(candle.low for candle in prior)

        trigger_slice = entry_candles[-self.trigger_window:]
        breakout_up = max(candle.close for candle in trigger_slice) > recent_high
        breakout_down = min(candle.close for candle in trigger_slice) < recent_low

        volume_avg = pd.Series([candle.volume for candle in entry_candles]).rolling(self.volume_lookback).mean() # tick volume on forex

        if pd.isna(volume_avg.iloc[-1]):

            return StrategyResult(
                signal=SignalType.NONE,
                reason="Invalid entry volume values",
            )

        volume_avg_v = float(volume_avg.iloc[-1])

        def decisive(candle, bullish): # decisive body + volume on any candle in the trigger window
            candle_range = candle.high - candle.low
            body = abs(candle.close - candle.open)
            body_ratio = (body / candle_range) if candle_range > 0 else 0.0

            if body_ratio < self.min_body_ratio:

                return False

            if candle.volume < volume_avg_v * self.volume_multiplier:

                return False

            return candle.close > candle.open if bullish else candle.close < candle.open

        bullish_trigger = any(decisive(candle, True) for candle in trigger_slice)
        bearish_trigger = any(decisive(candle, False) for candle in trigger_slice)

        # CONTEXT TIMEFRAME

        context_bullish = True
        context_bearish = True

        if context_candles:

            context_closes = [
                candle.close
                for candle in context_candles
            ]
            context_close_series = pd.Series(context_closes)

            context_ema = context_close_series.ewm(span=self.context_ema, adjust=False, min_periods=self.context_ema).mean()
            context_ema_v = context_ema.iloc[-1]

            if pd.isna(context_ema_v):

                return StrategyResult(
                    signal=SignalType.NONE,
                    reason="Invalid context EMA values",
                )

            context_price = context_candles[-1].close
            context_bullish = context_price > context_ema_v # directional bias only, no slope gate
            context_bearish = context_price < context_ema_v

        # VALIDATE CONDITIONS

        if (
            trend_bullish
            and context_bullish
            and (momentum_bullish or breakout_up)
            and bullish_trigger
        ):

            return StrategyResult(signal=SignalType.BUY)

        if (
            trend_bearish
            and context_bearish
            and (momentum_bearish or breakout_down)
            and bearish_trigger
        ):

            return StrategyResult(signal=SignalType.SELL)

        return StrategyResult(signal=SignalType.NONE)
