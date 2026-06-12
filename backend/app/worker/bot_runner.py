from datetime import datetime, timezone
import threading, time
from app.infrastructure.data_provider.mt5_provider import MT5Provider
from app.domain.services.strategy_engine import StrategyEngine
from app.infrastructure.ws.ws_manager import ws_manager
from app.domain.enums.enums import LogType, SignalType
from app.domain.models.models import SignalResult, LogEntry, MarketData
from app.infrastructure.notifications.telegram_notifier import TelegramNotifier
from app.infrastructure.data.signal_tracker import SignalTracker
from app.infrastructure.config.config_loader import ConfigLoader

class BotRunner:
    def __init__(self):
        self.running = False
        self.stop_event = threading.Event()
        self.provider = MT5Provider()
        self.engine = StrategyEngine()
        self.telegram_notifier = TelegramNotifier()
        self.signal_tracker = SignalTracker()
        self.config_loader = ConfigLoader()
        self.interval = 30

    def start(self):
        self.running = True
        self.stop_event.clear()

        while self.running:
            cycle_start = time.time()

            try:
                self._run_cycle()
            except Exception as e:
                self._log_error(f"Error in bot runner: {e}")

            self._handle_cycle_timing(cycle_start)

    def stop(self):
        self.running = False
        self.stop_event.set()

    def _run_cycle(self):
        config = self.config_loader.load()
        self.interval = max(30, config.execution_interval)
        active_configs = [c for c in config.configurations if c.enabled]

        if not active_configs:
            self._log_info("No active configurations, add or enable one")
            return

        for configuration in active_configs:
            self._process_configuration(configuration)

    def _process_configuration(self, configuration):
        if not configuration.symbols:
            self._log_info(f"No symbols configured, skipping configuration. id: {configuration.id}")
            return

        for symbol in configuration.symbols:
            self._process_symbol(symbol, configuration)

    def _process_symbol(self, symbol, configuration):
        try:
            data = self._fetch_market_data(symbol, configuration)

            for strategy in configuration.strategies:
                self._execute_strategy(strategy, symbol, configuration, data)

        except Exception as e:
            self._log_error(f"Error processing symbol {symbol} id: {configuration.id} - {str(e)}")

    def _fetch_market_data(self, symbol, configuration):
        return MarketData(
            trend = self.provider.get_data(symbol, configuration.timeframes.trend),
            entry = self.provider.get_data(symbol, configuration.timeframes.entry, 50)
        )
    
    def _execute_strategy(self, strategy, symbol, configuration, data):
        signal, logs = self.engine.run(strategy, data)
        self._send_logs(logs)

        if signal == SignalType.HOLD:
            return

        candle_time = data.trend.index[-1]
        price = data.entry["close"].iloc[-1]

        if self._is_duplicate_signal(symbol, strategy, configuration.timeframes.trend, candle_time):
            return
        
        self._send_notifications(signal, symbol, configuration, strategy, price)

    def _send_notifications(self, signal, symbol, configuration, strategy, price):
        self.telegram_notifier.send(signal, symbol, configuration.timeframes.trend, strategy, price)
        self._send_signal(signal, symbol, configuration.timeframes.trend, strategy, price)

    def _is_duplicate_signal(self, symbol, strategy, timeframe, candle_time):
        key = f"{symbol}_{strategy}_{timeframe}"
        return self.signal_tracker.is_duplicate(key, str(candle_time))
    
    def _send_signal(self, signal, symbol, temporality, strategy, price=0):
        self._send_ws(
            SignalResult(
                symbol=symbol,
                strategy=strategy.value,
                timestamp=datetime.now(timezone.utc).isoformat(),
                signal=signal.value,
                temporality=temporality.value,
                price=round(price, 2)
            )
        )

    def _log(self, level, message):
        self._send_ws(
            LogEntry(
                level=level.value,
                message=message,
                timestamp=datetime.now(timezone.utc).isoformat()
            )
        )

    def _log_info(self, message):
        self._log(LogType.INFO, message)
        
    def _log_error(self, message):
        self._log(LogType.ERROR, message)

    def _send_logs(self, logs):
        if not logs:
            return

        for log in logs:
            self._send_ws(log)

    def _send_ws(self, message):
        ws_manager.send(message.model_dump())

    def _handle_cycle_timing(self, cycle_start):
        cycle_duration = (time.time() - cycle_start)

        if cycle_duration > self.interval:
            self._log_error(f"Analysis duration exceeded interval: {cycle_duration:.2f}s > {self.interval}s")

        remaining = max(0, self.interval - cycle_duration)

        if self.stop_event.wait(timeout=remaining):
            self.running = False
