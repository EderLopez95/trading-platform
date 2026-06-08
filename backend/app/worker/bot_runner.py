from datetime import datetime, timezone
import threading, time
from app.infrastructure.config.config_loader import load_config
from app.infrastructure.data_provider.mt5_provider import MT5Provider
from app.domain.services.strategy_engine import StrategyEngine
from app.infrastructure.ws.ws_manager import ws_manager
from app.domain.enums.enums import LogType, SignalType
from app.domain.models.models import SignalResult, LogEntry, MarketData
from app.infrastructure.notifications.telegram_notifier import TelegramNotifier
from app.infrastructure.notifications.local_notifier import LocalNotifier

class BotRunner:
    def __init__(self):
        self.running = False
        self.stop_event = threading.Event()
        self.provider = MT5Provider()
        self.engine = StrategyEngine()
        self.telegram_notifier = TelegramNotifier()
        self.local_notifier = LocalNotifier()
        self.last_signal_candle = {}

    def _send_ws(self, message):
        ws_manager.send(message.model_dump())

    def _send_signal(self, signal, symbol, temporality, strategy, price=0):
        self._send_ws(
            SignalResult(
                symbol = symbol,
                strategy = strategy.value,
                timestamp = datetime.now(timezone.utc).isoformat(),
                signal = signal.value,
                temporality = temporality.value,
                price = round(price, 2)
            )
        )

    def start(self):
        self.running = True
        self.stop_event.clear()

        while self.running:
            cycle_start = time.time()

            try:
                config = load_config()
                active_configs = [c for c in config.configurations if c.enabled]
                interval = max(30, config.execution_interval) # ensure minimum interval of 30 seconds to prevent overload

                if active_configs and len(active_configs) > 0:
                    for configuration in active_configs:
                        symbols = configuration.symbols

                        if len(symbols) == 0:
                            self._send_ws(LogEntry(
                                level = LogType.ERROR.value,
                                message = f"No symbols configured, skipping cycle. id: {configuration.id}",
                                timestamp = datetime.now(timezone.utc).isoformat()
                            ))
                        else:
                            for symbol in symbols:
                                # fetch market data from provider for specific symbol and timeframes
                                data = MarketData(
                                    trend = self.provider.get_data(symbol, configuration.timeframes.trend),
                                    entry = self.provider.get_data(symbol, configuration.timeframes.entry, 50) # minimum data required
                                )
                                try:
                                    for strategy in configuration.strategies:
                                        # execute analysis and strategy
                                        signal, logs = self.engine.run(strategy, data)
                                        
                                        # in case of logs or signals, send to ws and notifier
                                        if logs:
                                            for log in logs:
                                                self._send_ws(log)
                                        
                                        if signal != SignalType.HOLD:
                                            # send signal only if it is a new candle to prevent duplicates
                                            candle_time = data.trend.index[-1]
                                            last_candle = self.last_signal_candle.get(symbol)
                                            
                                            if last_candle == candle_time:
                                                continue
                                            
                                            self.last_signal_candle[symbol] = candle_time
                                            price = data.entry["close"].iloc[-1]
                                            
                                            # notifications
                                            self.telegram_notifier.send(signal, symbol, configuration.timeframes.trend, strategy, price)
                                            self.local_notifier.send(signal, symbol)
                                            self._send_signal(signal, symbol, configuration.timeframes.trend, strategy, price)

                                except Exception as e:
                                    self._send_ws(LogEntry(
                                        level = LogType.ERROR.value,
                                        message = f"Error processing symbol {symbol} id: {configuration.id} - {str(e)}",
                                        timestamp = datetime.now(timezone.utc).isoformat()
                                    ))
                else:
                    self._send_ws(LogEntry(
                        level = LogType.INFO.value,
                        message = "No configurations, add new one",
                        timestamp = datetime.now(timezone.utc).isoformat()
                    ))

                cycle_duration = time.time() - cycle_start
                remaining = max(0, interval - cycle_duration)

                if cycle_duration > interval:
                    self._send_ws(LogEntry(
                        level = LogType.INFO.value,
                        message = f"Analysis duration exceeded interval: {cycle_duration:.2f}s > {interval}s",
                        timestamp = datetime.now(timezone.utc).isoformat()
                    ))

                if self.stop_event.wait(timeout=remaining):
                    break
                
            except Exception as e:
                self._send_ws(LogEntry(
                    level = LogType.ERROR.value,
                    message = f"Error in bot runner: {str(e)}",
                    timestamp = datetime.now(timezone.utc).isoformat()
                ))

    def stop(self):
        self.running = False
        self.stop_event.set()
