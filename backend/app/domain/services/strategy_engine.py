from datetime import datetime, timezone
from app.domain.strategies.multi_smas_momentum_strategy import MultiSMAsMomentumStrategy
from app.domain.strategies.rsi_cross_trend_strategy import RSICrossTrendStrategy
from app.domain.strategies.rsi_dip_accumulation_strategy import RSIDipAccumulationStrategy
from app.domain.enums.enums import StrategyType, SignalType, LogType
from app.domain.models.models import LogEntry

class StrategyEngine:
    def __init__(self):
        # add strategies from strategies folder, they must implement an execute method that returns a signal
        self.strategies = {
            StrategyType.RSI_CROSS_TREND: RSICrossTrendStrategy(),
            StrategyType.MULTI_SMAS_MOMENTUM: MultiSMAsMomentumStrategy(),
            StrategyType.RSI_DIP_ACCUMULATION: RSIDipAccumulationStrategy()
        }
        self.default_strategy = StrategyType.RSI_CROSS_TREND

    def _add_log(self, logs, level, message):
        logs.append(LogEntry(
            level = level,
            message = message,
            timestamp = datetime.now(timezone.utc).isoformat()
        ))

    def run(self, strategy, data):
        strat = self.strategies.get(strategy)
        logs = []

        if strat is None:
            self._add_log(logs, LogType.INFO.value, f"Strategy '{strategy.value}' not found. Using default '{self.default_strategy.value}'")
            strat = self.strategies[self.default_strategy]

        try:
            signal = strat.execute(data)

            if signal not in [SignalType.BUY, SignalType.SELL, SignalType.HOLD]:
                self._add_log(logs, LogType.INFO.value, f"Invalid signal '{signal}', defaulting to HOLD")
                return SignalType.HOLD, logs
            
            return signal, logs
        except Exception as e:
            self._add_log(logs, LogType.ERROR.value, f"Error executing strategy '{strategy.value}': {e}")
            return SignalType.HOLD, logs
