import grpc
from app.infrastructure.protos.generated import signal_pb2, signal_pb2_grpc
from app.config.settings import SIGNAL_SERVICE_HOST, SIGNAL_SERVICE_PORT

class SignalClient:
    def __init__(self):
        target = (f"{SIGNAL_SERVICE_HOST}:{SIGNAL_SERVICE_PORT}")
        self.channel = grpc.insecure_channel(target)
        self.stub = signal_pb2_grpc.SignalServiceStub(self.channel)

    def create_configuration(
        self,
        user_id: str,
        symbols: list[str],
        strategies: list[str],
        trend_timeframe: str,
        context_timeframe: str,
        entry_timeframe: str,
    ):
        request = (
            signal_pb2.CreateConfigurationRequest(
                user_id=user_id,
                symbols=symbols,
                strategies=strategies,
                trend_timeframe=trend_timeframe,
                context_timeframe=context_timeframe,
                entry_timeframe=entry_timeframe,
            )
        )

        return self.stub.CreateConfiguration(request)
    
    def get_configurations(self, user_id: str):
        request = signal_pb2.GetConfigurationsRequest(user_id=user_id)

        return self.stub.GetConfigurations(request)
    
    def delete_configuration(self, configuration_id: str):
        request = signal_pb2.DeleteConfigurationRequest(configuration_id=configuration_id)

        return self.stub.DeleteConfiguration(request)
    
    def toggle_configuration(self, configuration_id: str, enabled: bool):
        request = signal_pb2.ToggleConfigurationRequest(
            configuration_id=configuration_id,
            enabled=enabled
        )

        return self.stub.ToggleConfiguration(request)
