import logging
from google.protobuf.empty_pb2 import Empty
from app.infrastructure.database.connection import SessionLocal
from app.infrastructure.protos.generated import signal_pb2, signal_pb2_grpc
import queue
from app.infrastructure.streaming.signal_broadcaster import signal_broadcaster
from app.infrastructure.database.repositories.configuration_repository import ConfigurationRepositoryImpl
from app.infrastructure.grpc.mappers.configuration_grpc_mapper import ConfigurationGrpcMapper
from app.application.services.configuration_service import ConfigurationService
from app.application.services.user_settings_service import UserSettingsService
from app.infrastructure.database.repositories.user_settings_repository import UserSettingsRepositoryImpl
from app.infrastructure.database.repositories.signal_repository import SignalRepositoryImpl
from app.infrastructure.grpc.mappers.signal_mapper import SignalMapper
from app.application.services.get_signals_service import GetSignalsService
from app.application.services.registry_refresh_service import RegistryRefreshService
from app.application.services.user_registry_service import UserRegistryService
from app.application.services.configuration_registry_service import ConfigurationRegistryService
from app.application.services.user_profile_registry_service import UserProfileRegistryService
from app.infrastructure.scheduler.registry_container import user_registry, configuration_registry, user_profile_registry
from app.infrastructure.grpc.clients.auth_client import AuthClient
from app.application.services.strategy_service import StrategyService
from app.application.services.symbol_service import SymbolService
from app.application.services.timeframe_service import TimeframeService
from app.infrastructure.grpc.clients.market_data_client import MarketDataClient

logger = logging.getLogger("signal")
user_settings_repository = UserSettingsRepositoryImpl(SessionLocal())

class SignalGrpcService(signal_pb2_grpc.SignalServiceServicer):
    def CreateConfiguration(self, request, context):
        request_id = _get_request_id(context)
        logger.info(
            "create_configuration_called",
            extra={
                "request_id": request_id,
                "service": "signal",
            }
        )

        with SessionLocal() as db:
            repository = ConfigurationRepositoryImpl(db)
            use_case = ConfigurationService(repository)

            configuration = (
                use_case.create_configuration(
                    user_id=request.user_id,
                    symbols=list(request.symbols),
                    strategies=list(request.strategies),
                    trend_timeframe=request.trend_timeframe,
                    context_timeframe=request.context_timeframe,
                    entry_timeframe=request.entry_timeframe,
                )
            )

            return (
                signal_pb2.ConfigurationResponse(
                    configuration=ConfigurationGrpcMapper.to_proto(configuration)
                )
            )

    def GetConfigurations(self, request, context):
        request_id = _get_request_id(context)
        logger.info(
            "get_configurations_called",
            extra={
                "request_id": request_id,
                "service": "signal",
            }
        )

        with SessionLocal() as db:
            repository = ConfigurationRepositoryImpl(db)
            use_case = ConfigurationService(repository)

            configurations = use_case.get_configurations(
                request.user_id
            )

            return (
                signal_pb2.ConfigurationListResponse(
                    configurations=[
                        ConfigurationGrpcMapper.to_proto(
                            configuration
                        )
                        for configuration in configurations
                    ]
                )
            )

    def UpdateConfiguration(self, request, context):
        request_id = _get_request_id(context)
        logger.info(
            "update_configuration_called",
            extra={
                "request_id": request_id,
                "service": "signal",
            }
        )

        with SessionLocal() as db:
            repository = ConfigurationRepositoryImpl(db)
            use_case = ConfigurationService(repository)

            configuration = (
                use_case.update_configuration(
                    configuration_id=request.configuration_id,
                    symbols=list(request.symbols),
                    strategies=list(request.strategies),
                    trend_timeframe=request.trend_timeframe,
                    context_timeframe=request.context_timeframe,
                    entry_timeframe=request.entry_timeframe,
                )
            )

            return (
                signal_pb2.ConfigurationResponse(
                    configuration=ConfigurationGrpcMapper.to_proto(configuration)
                )
            )

    def DeleteConfiguration(self, request, context):
        request_id = _get_request_id(context)
        logger.info(
            "delete_configuration_called",
            extra={
                "request_id": request_id,
                "service": "signal",
            }
        )

        with SessionLocal() as db:
            repository = ConfigurationRepositoryImpl(db)
            use_case = ConfigurationService(repository)

            use_case.delete_configuration(request.configuration_id)

            return Empty()

    def ToggleConfiguration(self, request, context):
        request_id = _get_request_id(context)
        logger.info(
            "toggle_configuration_called",
            extra={
                "request_id": request_id,
                "service": "signal",
            }
        )

        with SessionLocal() as db:
            repository = ConfigurationRepositoryImpl(db)
            use_case = ConfigurationService(repository)

            configuration = use_case.toggle_configuration(
                request.configuration_id,
                request.enabled,
            )

            return (
                signal_pb2.ConfigurationResponse(
                    configuration=ConfigurationGrpcMapper.to_proto(configuration)
                )
            )

    def GetAnalysisStatus(self, request, context):
        request_id = _get_request_id(context)
        logger.info(
            "get_analysis_status_called",
            extra={
                "request_id": request_id,
                "service": "signal",
            }
        )

        with SessionLocal() as db:
            repository = UserSettingsRepositoryImpl(db)
            service = UserSettingsService(repository)
            settings = service.get_status(request.user_id)

            return (
                signal_pb2.AnalysisStatusResponse(
                    enabled=settings.analysis_enabled
                )
            )

    def ToggleAnalysis(self, request, context):
        request_id = _get_request_id(context)
        logger.info(
            "toggle_analysis_called",
            extra={
                "request_id": request_id,
                "service": "signal",
            }
        )

        with SessionLocal() as db:
            repository = UserSettingsRepositoryImpl(db)
            service = UserSettingsService(repository)
            
            settings = (
                service.toggle_analysis(
                    request.user_id,
                    request.enabled,
                )
            )

            return (
                signal_pb2.AnalysisStatusResponse(
                    enabled=settings.analysis_enabled
                )
            )
        
    def GetSignals(self, request, context):
        request_id = _get_request_id(context)
        logger.info(
            "get_signals_called",
            extra={
                "request_id": request_id,
                "service": "signal",
            }
        )

        with SessionLocal() as db:
            repository = SignalRepositoryImpl(db)
            service = GetSignalsService(repository)

            result = service.execute(
                user_id=request.user_id,
                symbol=request.symbol or None,
                strategy=request.strategy or None,
                page=request.page,
                page_size=request.page_size,
            )

            return (
                signal_pb2.GetSignalsResponse(
                    signals=[
                        SignalMapper.to_proto(signal)
                        for signal in result["items"]
                    ],
                    page=request.page,
                    page_size=request.page_size,
                    total=result["total"],
                )
            )

    def StreamSignals(self, request, context):
        request_id = _get_request_id(context)
        logger.info(
            "stream_signals_called",
            extra={
                "request_id": request_id,
                "service": "signal",
            }
        )

        subscriber_id, subscriber_queue = signal_broadcaster.subscribe(request.user_id)

        try:
            while context.is_active():
                try:
                    signal = subscriber_queue.get(timeout=1)
                except queue.Empty:
                    continue

                yield SignalMapper.to_proto(signal)
        finally:
            signal_broadcaster.unsubscribe(subscriber_id)

    def RefreshRegistries(self, request, context):
        request_id = _get_request_id(context)
        logger.info(
            "refresh_registries_called",
            extra={
                "request_id": request_id,
                "service": "signal",
            }
        )

        with SessionLocal() as db:
            configuration_repository = ConfigurationRepositoryImpl(db)

            result = RegistryRefreshService(
                user_service=UserRegistryService(user_settings_repository, user_registry),
                profile_service=UserProfileRegistryService(AuthClient(), user_profile_registry),
                configuration_service=ConfigurationRegistryService(configuration_repository, configuration_registry),
            ).refresh()

            logger.info(
                "refresh_registries_completed",
                extra={
                    "request_id": request_id,
                    "users": user_registry.count(),
                    "profiles": user_profile_registry.count(),
                    "configurations": result["configurations"]["loaded"],
                    "excluded_configurations": result["configurations"]["excluded"],
                    "service": "signal",
                }
            )

            return signal_pb2.RefreshRegistriesResponse(success=True)

    def GetStrategies(self, request, context):
        request_id = _get_request_id(context)
        logger.info(
            "get_strategies_called",
            extra={
                "request_id": request_id,
                "service": "signal",
            }
        )

        strategies = StrategyService().get_all()

        return (
            signal_pb2.GetStrategiesResponse(
                strategies=[
                    signal_pb2.StrategyDto(
                        id=strategy["id"],
                        name=strategy["name"],
                    )
                    for strategy in strategies
                ]
            )
        )
    
    def GetSymbols(self, request, context):
        request_id = _get_request_id(context)
        logger.info(
            "get_symbols_called",
            extra={
                "request_id": request_id,
                "service": "signal",
            }
        )

        symbols = SymbolService(MarketDataClient()).get_all(request.search or None)

        return signal_pb2.GetSymbolsResponse(
            symbols=[
                signal_pb2.SymbolDto(symbol=symbol)
                for symbol in symbols
            ]
        )

    def GetTimeframes(self, request, context):
        request_id = _get_request_id(context)
        logger.info(
            "get_timeframes_called",
            extra={
                "request_id": request_id,
                "service": "signal",
            }
        )

        timeframes = TimeframeService().get_all()

        return signal_pb2.GetTimeframesResponse(
            timeframes=[
                signal_pb2.TimeframeDto(timeframe=timeframe)
                for timeframe in timeframes
            ]
        )

def _get_request_id(context):
    metadata = dict(context.invocation_metadata())
    
    return metadata.get("request-id")
