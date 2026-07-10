from app.domain.enums.enums import SignalType
from app.domain.entities.strategy_result import StrategyResult
from app.domain.indicators.ema import calculate_ema_series

class EmaCrossStrategy:
    FAST_EMA = 20
    SLOW_EMA = 50

    def evaluate(self, candles):
        closes = [
            candle.close
            for candle in candles
        ]

        if len(closes) < self.SLOW_EMA + 2:

            return StrategyResult(
                signal=SignalType.NONE,
                reason="Not enough candles",
            )

        fast = calculate_ema_series(closes, self.FAST_EMA)
        slow = calculate_ema_series(closes, self.SLOW_EMA)

        if len(fast) < 2:
            return StrategyResult(signal=SignalType.NONE)

        if len(slow) < 2:
            return StrategyResult(signal=SignalType.NONE)

        previous_fast = fast[-2]
        current_fast = fast[-1]
        previous_slow = slow[-2]
        current_slow = slow[-1]

        cross_up = (
            previous_fast <= previous_slow
            and current_fast > current_slow
        )

        cross_down = (
            previous_fast >= previous_slow
            and current_fast < current_slow
        )

        if cross_up:

            return StrategyResult(signal=SignalType.BUY)

        if cross_down:

            return StrategyResult(signal=SignalType.SELL)
            
        return StrategyResult(signal=SignalType.NONE)
