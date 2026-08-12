import time, logging, grpc
from app.infrastructure.database.connection import SessionLocal
from datetime import datetime, timezone
from app.infrastructure.scheduler.utils import should_execute, get_candle_key
from app.infrastructure.scheduler.registry_container import user_registry, configuration_registry
from app.infrastructure.adapters.market_data_adapter import MarketDataAdapter
from app.domain.enums.enums import SignalType
from app.infrastructure.scheduler.strategy_container import strategy_registry
from app.domain.formatters.signal_formatter import SignalFormatter
from app.infrastructure.notifications.telegram_adapter import TelegramAdapter
from app.application.services.notification_service import NotificationService
from app.infrastructure.notifications.notification_dispatcher import NotificationDispatcher
from app.infrastructure.scheduler.registry_container import user_profile_registry
from app.infrastructure.grpc.clients.auth_client import AuthClient
from app.application.services.user_profile_provider import UserProfileProvider
from app.application.services.signal_generation_service import SignalGenerationService
from app.infrastructure.database.repositories.signal_repository import SignalRepositoryImpl
from app.infrastructure.scheduler.metrics import SchedulerMetrics
from app.domain.constants.timeframes import TIMEFRAMES

logger = logging.getLogger("signal")

class SignalEngine:
    def __init__(self):
        self.market_data = MarketDataAdapter()
        self.notification_dispatcher = NotificationDispatcher(NotificationService(TelegramAdapter()))
        self.profile_provider = UserProfileProvider(AuthClient(), user_profile_registry)
        self._last_execution = {}

    def run(self):
        metrics = SchedulerMetrics()

        while True:
            try:    
                now = datetime.now(timezone.utc)

                with SessionLocal() as db:
                    signal_generation_service = SignalGenerationService(SignalRepositoryImpl(db))

                    for configuration in (configuration_registry.get_users()):
                        started_at = time.time()

                        if not (user_registry.is_analysis_enabled(configuration.user_id)):
                            continue

                        if not should_execute(configuration, now):
                            continue

                        execution_key = (get_candle_key(configuration, now))

                        if (self._last_execution.get(configuration.id) == execution_key):
                            continue

                        self._last_execution[configuration.id] = execution_key
                        user = self.profile_provider.get(configuration.user_id)

                        for symbol in (configuration.symbols):
                            try:
                                trend_candles_response = None
                                context_candles_response = None
                                entry_candles_response = None

                                if configuration.trend_timeframe and configuration.trend_timeframe in TIMEFRAMES:
                                    trend_candles_response = (
                                        self.market_data.get_candles(
                                            symbol=symbol,
                                            timeframe=configuration.trend_timeframe,
                                            count=100,
                                        )
                                    )

                                if configuration.context_timeframe and configuration.context_timeframe in TIMEFRAMES:
                                    context_candles_response = (
                                        self.market_data.get_candles(
                                            symbol=symbol,
                                            timeframe=configuration.context_timeframe,
                                            count=100,
                                        )
                                    )

                                if configuration.entry_timeframe and configuration.entry_timeframe in TIMEFRAMES:
                                    entry_candles_response = (
                                        self.market_data.get_candles(
                                            symbol=symbol,
                                            timeframe=configuration.entry_timeframe,
                                            count=50,
                                        )
                                    )

                                trend_candles = trend_candles_response.candles if trend_candles_response else None
                                context_candles = context_candles_response.candles if context_candles_response else None
                                entry_candles = entry_candles_response.candles if entry_candles_response else None

                                candle_time = (
                                    datetime.fromtimestamp(
                                        trend_candles[-1].timestamp,
                                        tz=timezone.utc
                                    )
                                    if trend_candles else now
                                )

                                for strategy_name in (configuration.strategies):
                                    strategy = strategy_registry.get(strategy_name)

                                    if not strategy:
                                        continue

                                    result = strategy.evaluate(trend_candles, context_candles, entry_candles)

                                    if result.reason:
                                        logger.info(
                                            "strategy_evaluation",
                                            extra={
                                                "configuration_id": configuration.id,
                                                "symbol": symbol,
                                                "strategy": strategy_name,
                                                "reason": result.reason,
                                            }
                                        )

                                    if result.signal == SignalType.NONE:
                                        continue

                                    signal = (
                                        signal_generation_service.generate(
                                            configuration=configuration,
                                            symbol=symbol,
                                            strategy=strategy_name,
                                            result=result,
                                            candle_time=candle_time,
                                            price=trend_candles[-1].close if trend_candles else 0,
                                        )
                                    )

                                    if not signal:
                                        continue

                                    metrics.signals += 1

                                    if not user or not user.telegram_token or not user.telegram_chat_id:
                                        continue

                                    message = (
                                        SignalFormatter.telegram(
                                            symbol=symbol,
                                            strategy=strategy_name,
                                            signal=result.signal.value,
                                            trend_timeframe=configuration.trend_timeframe,
                                            context_timeframe=configuration.context_timeframe if configuration.context_timeframe else "",
                                            entry_timeframe=configuration.entry_timeframe,
                                            price=trend_candles[-1].close if trend_candles else 0,
                                        )
                                    )

                                    self.notification_dispatcher.enqueue(
                                        token=user.telegram_token,
                                        chat_id=user.telegram_chat_id,
                                        message=message,
                                    )

                            except grpc.RpcError as e:
                                logger.error(
                                    "Error in signal engine for configuration",
                                    extra={
                                        "configuration_id": configuration.id,
                                        "symbol": symbol,
                                        "status": e.code().name,
                                        "details": e.details(),
                                    }
                                )
                                metrics.errors += 1
                                continue

                        duration = time.time() - started_at
                        logger.info(
                            "scheduler_cycle",
                            extra={
                                "signals": metrics.signals,
                                "errors": metrics.errors,
                                "duration_ms": round(duration * 1000, 2),
                            }
                        )

            except Exception as e:
                logger.error(
                    "Error in signal engine",
                    extra={
                        "error": str(e),
                    }
                )
                metrics.errors += 1

            time.sleep(60)
