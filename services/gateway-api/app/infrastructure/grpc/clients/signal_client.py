import grpc
from app.infrastructure.protos.generated import signal_pb2, signal_pb2_grpc
from app.config.settings import SIGNAL_SERVICE_HOST, SIGNAL_SERVICE_PORT, GATEWAY_SERVICE_SECURE, GATEWAY_SERVICE_CERT
from app.infrastructure.grpc.error_mapper import map_grpc_error

class SignalClient:
    def __init__(self):
        address = (f"{SIGNAL_SERVICE_HOST}:{SIGNAL_SERVICE_PORT}")

        if GATEWAY_SERVICE_SECURE:
            with open(GATEWAY_SERVICE_CERT, "rb") as f:
                credentials = grpc.ssl_channel_credentials(f.read())
            self.channel = grpc.secure_channel(address, credentials)
        else:
            self.channel = grpc.insecure_channel(address)

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
        try:
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
        
        except grpc.RpcError as e:
            map_grpc_error(e)
    
    def get_configurations(self, user_id: str):
        try:
            request = signal_pb2.GetConfigurationsRequest(user_id=user_id)

            return self.stub.GetConfigurations(request)
        
        except grpc.RpcError as e:
            map_grpc_error(e)
    
    def delete_configuration(self, configuration_id: str):
        try:
            request = signal_pb2.DeleteConfigurationRequest(configuration_id=configuration_id)

            return self.stub.DeleteConfiguration(request)
        
        except grpc.RpcError as e:
            map_grpc_error(e)
    
    def toggle_configuration(self, configuration_id: str, enabled: bool):
        try:
            request = signal_pb2.ToggleConfigurationRequest(
                configuration_id=configuration_id,
                enabled=enabled
            )

            return self.stub.ToggleConfiguration(request)
        
        except grpc.RpcError as e:
            map_grpc_error(e)

    def get_analysis_status(self, user_id: str):
        try:
            request = signal_pb2.AnalysisStatusRequest(user_id=user_id)

            return self.stub.GetAnalysisStatus(request)
        
        except grpc.RpcError as e:
            map_grpc_error(e)
    
    def toggle_analysis(self, user_id: str, enabled: bool):
        try:
            request = (
                signal_pb2.ToggleAnalysisRequest(
                    user_id=user_id,
                    enabled=enabled
                )
            )

            return self.stub.ToggleAnalysis(request)
        
        except grpc.RpcError as e:
            map_grpc_error(e)
