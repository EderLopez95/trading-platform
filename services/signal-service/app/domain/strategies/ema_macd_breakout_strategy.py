from app.domain.enums.enums import SignalType
from app.domain.entities.strategy_result import StrategyResult
from app.domain.indicators.macd import MACD
import pandas as pd

class EMAMACDBreakoutStrategy:
    def __init__(
        self,
        ema_fast=9,
        ema_mid=21,
        ema_slow=50,
        context_ema=50,
        breakout_lookback=20,
        min_body_ratio=0.5,
    ):
        self.macd = MACD()
        self.ema_fast = ema_fast
        self.ema_mid = ema_mid
        self.ema_slow = ema_slow
        self.context_ema = context_ema
        self.breakout_lookback = breakout_lookback
        self.min_body_ratio = min_body_ratio

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

        if not entry_candles or len(entry_candles) < max(entry_min, self.breakout_lookback + 1):

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

        if pd.isna(ema_slow_v) or pd.isna(ema_fast.iloc[-3]):

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

        ema_fast_prev = ema_fast.iloc[-3] # slope of the fast EMA confirms the move is in progress (not flat)
        trend_rising = ema_fast_v > ema_fast_prev
        trend_falling = ema_fast_v < ema_fast_prev

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
        hist_v = float(histogram.iloc[-1])

        momentum_bullish = (
            macd_v > signal_v
            and hist_v > 0
            and self.macd.rising(histogram)
        )
        momentum_bearish = (
            macd_v < signal_v
            and hist_v < 0
            and self.macd.falling(histogram)
        )

        window = entry_candles[-(self.breakout_lookback + 1):-1] # breakout of the recent range, excluding the current (last) candle
        recent_high = max(candle.high for candle in window)
        recent_low = min(candle.low for candle in window)

        last = entry_candles[-1]
        breakout_up = last.close > recent_high
        breakout_down = last.close < recent_low

        candle_range = last.high - last.low # decisive candle body confirms conviction behind the breakout
        body = abs(last.close - last.open)
        body_ratio = (body / candle_range) if candle_range > 0 else 0.0
        bullish_candle = last.close > last.open and body_ratio >= self.min_body_ratio
        bearish_candle = last.close < last.open and body_ratio >= self.min_body_ratio

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

            if pd.isna(context_ema_v) or pd.isna(context_ema.iloc[-3]):

                return StrategyResult(
                    signal=SignalType.NONE,
                    reason="Invalid context EMA values",
                )

            context_price = context_candles[-1].close
            context_ema_prev = context_ema.iloc[-3]
            context_bullish = context_price > context_ema_v and context_ema_v >= context_ema_prev
            context_bearish = context_price < context_ema_v and context_ema_v <= context_ema_prev

        # VALIDATE CONDITIONS

        if (
            trend_bullish
            and trend_rising
            and context_bullish
            and momentum_bullish
            and breakout_up
            and bullish_candle
        ):

            return StrategyResult(signal=SignalType.BUY)

        if (
            trend_bearish
            and trend_falling
            and context_bearish
            and momentum_bearish
            and breakout_down
            and bearish_candle
        ):

            return StrategyResult(signal=SignalType.SELL)

        return StrategyResult(signal=SignalType.NONE)
