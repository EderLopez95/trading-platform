import grpc
from app.infrastructure.protos.generated import signal_pb2, signal_pb2_grpc
from app.config.settings import ENV, SIGNAL_SERVICE_HOST, SIGNAL_SERVICE_PORT, GATEWAY_SERVICE_SECURE, TRUSTED_CA_CERT
from app.infrastructure.grpc.error_mapper import map_grpc_error

class SignalClient:
    def __init__(self):
        address = (f"{SIGNAL_SERVICE_HOST}:{SIGNAL_SERVICE_PORT}")

        if ENV == "prod" and GATEWAY_SERVICE_SECURE:
            with open(TRUSTED_CA_CERT, "rb") as f:
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

    def update_configuration(
        self,
        configuration_id: str,
        symbols: list[str],
        strategies: list[str],
        trend_timeframe: str,
        context_timeframe: str | None,
        entry_timeframe: str,
    ):
        try:
            request = signal_pb2.UpdateConfigurationRequest(
                configuration_id=configuration_id,
                symbols=symbols,
                strategies=strategies,
                trend_timeframe=trend_timeframe,
                context_timeframe=context_timeframe,
                entry_timeframe=entry_timeframe,
            )

            return self.stub.UpdateConfiguration(request)
        
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

    def get_signals(
        self,
        user_id: str,
        symbol: str | None,
        strategy: str | None,
        page: int,
        page_size: int,
    ):
        try:

            return self.stub.GetSignals(
                signal_pb2.GetSignalsRequest(
                    user_id=user_id,
                    symbol=symbol or "",
                    strategy=strategy or "",
                    page=page,
                    page_size=page_size,
                )
            )

        except grpc.RpcError as e:
            map_grpc_error(e)

    def stream_signals(self, user_id: str):

        return self.stub.StreamSignals(
            signal_pb2.StreamSignalsRequest(user_id=user_id)
        )

    def refresh_registries(self):
        try:

            return self.stub.RefreshRegistries(
                signal_pb2.RefreshRegistriesRequest()
            )

        except grpc.RpcError as e:
            map_grpc_error(e)

    def get_strategies(self):
        try:

            return self.stub.GetStrategies(signal_pb2.GetStrategiesRequest())
        
        except grpc.RpcError as e:
            map_grpc_error(e)

    def get_symbols(self, search: str | None = None):
        try:
        
            return self.stub.GetSymbols(signal_pb2.GetSymbolsRequest(search=search or ""))

        except grpc.RpcError as e:
            map_grpc_error(e)

    def get_timeframes(self):
        try:

            return self.stub.GetTimeframes(signal_pb2.GetTimeframesRequest())
        
        except grpc.RpcError as e:
            map_grpc_error(e)
