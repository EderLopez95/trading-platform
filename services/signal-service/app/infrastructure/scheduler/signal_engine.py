import time, logging, grpc
from app.infrastructure.database.connection import SessionLocal
from datetime import datetime, timezone
from app.infrastructure.scheduler.utils import should_execute, get_candle_key
from app.infrastructure.scheduler.registry_container import user_registry, configuration_registry
from app.infrastructure.adapters.market_data_adapter import MarketDataAdapter
from app.domain.enums.enums import SignalType
from app.domain.strategies.strategy_registry import STRATEGIES
from app.domain.formatters.signal_formatter import SignalFormatter
from app.infrastructure.notifications.telegram_adapter import TelegramAdapter
from app.application.services.notification_service import NotificationService
from app.infrastructure.scheduler.registry_container import user_profile_registry
from app.application.services.signal_generation_service import SignalGenerationService
from app.infrastructure.database.repositories.signal_repository import SignalRepositoryImpl

logger = logging.getLogger("signal")

class SignalEngine:
    def __init__(self):
        self.signal_generation_service = SignalGenerationService(SignalRepositoryImpl(SessionLocal()))
        self.market_data = MarketDataAdapter()
        self.notification_service = NotificationService(TelegramAdapter())
        self._last_execution = {}

    def run(self):
        while True:
            try:    
                now = datetime.now(timezone.utc)

                for configuration in (configuration_registry.get_all()):

                    if not (user_registry.is_analysis_enabled(configuration.user_id)):
                        continue

                    if not should_execute(configuration, now):
                        continue

                    execution_key = (get_candle_key(configuration, now))

                    if (self._last_execution.get(configuration.id) == execution_key):
                        continue

                    self._last_execution[configuration.id] = execution_key
                    user = user_profile_registry.get(configuration.user_id)
                    
                    for symbol in (configuration.symbols):
                        try:
                            candles_response = (
                                self.market_data.get_candles(
                                    symbol=symbol,
                                    timeframe=configuration.entry_timeframe,
                                    count=100,
                                )
                            )

                            candles = candles_response.candles

                            for strategy_name in (configuration.strategies):
                                strategy = STRATEGIES.get(strategy_name)

                                if not strategy:
                                    continue

                                result = strategy.evaluate(candles)

                                if result.signal == SignalType.NONE:
                                    continue

                                signal = (
                                    self.signal_generation_service.generate(
                                        configuration=configuration,
                                        symbol=symbol,
                                        strategy=strategy_name,
                                        result=result,
                                        candle_time=now,
                                        price=candles[-1].close,
                                    )
                                )

                                if not signal:
                                    continue

                                if not user or not user.telegram_token or not user.telegram_chat_id:
                                    continue

                                message = (
                                    SignalFormatter.telegram(
                                        symbol=symbol,
                                        strategy=strategy_name,
                                        signal=result.signal.value,
                                        timeframe=configuration.entry_timeframe,
                                        price=candles[-1].close,
                                    )
                                )

                                self.notification_service.send(
                                    token=user.telegram_token,
                                    chat_id=user.telegram_chat_id,
                                    message=message,
                                )

                        except grpc.RpcError as e:
                            logger.error(
                                "Unable to load candles",
                                extra={
                                    "configuration_id": configuration.id,
                                    "symbol": configuration.symbols[0],
                                    "status": e.code().name,
                                }
                            )
                            continue

            except Exception as ex:
                logger.error(
                    "Error in signal engine",
                    extra={
                        "error": str(ex),
                    }
                )

            time.sleep(60)
