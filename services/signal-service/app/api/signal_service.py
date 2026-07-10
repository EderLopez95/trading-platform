import logging
from google.protobuf.empty_pb2 import Empty
from app.infrastructure.database.connection import SessionLocal
from app.infrastructure.protos.generated import signal_pb2, signal_pb2_grpc
from app.infrastructure.database.repositories.configuration_repository import ConfigurationRepositoryImpl
from app.infrastructure.grpc.mappers.configuration_grpc_mapper import ConfigurationGrpcMapper
from app.application.services.configuration_service import ConfigurationService
from app.application.services.user_settings_service import UserSettingsService
from app.infrastructure.database.repositories.user_settings_repository import UserSettingsRepositoryImpl

logger = logging.getLogger("signal")

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

def _get_request_id(context):
    metadata = dict(context.invocation_metadata())
    
    return metadata.get("request-id")
