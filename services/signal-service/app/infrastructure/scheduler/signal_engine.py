import time
from datetime import datetime, timezone
from app.infrastructure.scheduler.utils import should_execute, get_candle_key
from app.infrastructure.scheduler.registry_container import user_registry, configuration_registry
from app.infrastructure.adapters.market_data_adapter import MarketDataAdapter

class SignalEngine:
    def __init__(self):
        self.market_data = (MarketDataAdapter())
        self._last_execution = {}

    def run(self):
        while True:
            now = datetime.now(timezone.utc)

            for configuration in (configuration_registry.get_all()):
                if not (user_registry.is_analysis_enabled(configuration.user_id)):
                    continue

                if not should_execute(configuration, now):
                    continue

                candle_key = get_candle_key(configuration, now)
                last_key = self._last_execution.get(configuration.id)

                if last_key == candle_key:
                    continue

                self._last_execution[configuration.id] = candle_key
                candles = (
                    self.market_data.get_candles(
                        symbol=configuration.symbols[0],
                        timeframe=configuration.entry_timeframe,
                        count=100,
                    )
                )
                print(f"{configuration.symbols[0]} CANDLES={len(candles.candles)}", flush=True)

            time.sleep(60)
