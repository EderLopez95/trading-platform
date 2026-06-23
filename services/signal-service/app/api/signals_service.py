from google.protobuf.empty_pb2 import Empty
from app.infrastructure.database.connection import SessionLocal
from app.infrastructure.protos.generated import signals_pb2, signals_pb2_grpc
from app.infrastructure.database.repositories.configuration_repository import ConfigurationRepositoryImpl
from app.infrastructure.grpc.mappers.configuration_grpc_mapper import ConfigurationGrpcMapper
from app.application.services.configuration_service import ConfigurationService

class SignalsGrpcService(signals_pb2_grpc.SignalsServiceServicer):
    def CreateConfiguration(
        self,
        request,
        context,
    ):
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
                signals_pb2.ConfigurationResponse(
                    configuration=ConfigurationGrpcMapper.to_proto(configuration)
                )
            )

    def GetConfigurations(
        self,
        request,
        context,
    ):
        with SessionLocal() as db:
            repository = ConfigurationRepositoryImpl(db)
            use_case = ConfigurationService(repository)

            configurations = use_case.get_configurations(
                request.user_id
            )

            return (
                signals_pb2.ConfigurationListResponse(
                    configurations=[
                        ConfigurationGrpcMapper.to_proto(
                            configuration
                        )
                        for configuration in configurations
                    ]
                )
            )

    def DeleteConfiguration(
        self,
        request,
        context,
    ):
        with SessionLocal() as db:
            repository = ConfigurationRepositoryImpl(db)
            use_case = ConfigurationService(repository)

            use_case.delete_configuration(request.configuration_id)

            return Empty()

    def ToggleConfiguration(
        self,
        request,
        context,
    ):
        with SessionLocal() as db:
            repository = ConfigurationRepositoryImpl(db)
            use_case = ConfigurationService(repository)

            configuration = use_case.toggle_configuration(
                request.configuration_id,
                request.enabled,
            )

            return (
                signals_pb2.ConfigurationResponse(
                    configuration=ConfigurationGrpcMapper.to_proto(configuration)
                )
            )
