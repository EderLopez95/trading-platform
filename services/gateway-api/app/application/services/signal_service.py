from app.infrastructure.grpc.clients.signal_client import SignalClient

class SignalService:
    def __init__(self, client: SignalClient):
        self.client = client

    def create_configuration(self, user_id, data):
        
        return (
            self.client.create_configuration(
                user_id=user_id,
                symbols=data.symbols,
                strategies=data.strategies,
                trend_timeframe=data.trend_timeframe,
                context_timeframe=data.context_timeframe,
                entry_timeframe=data.entry_timeframe,
            )
        )

    def get_configurations(self, user_id):

        return self.client.get_configurations(user_id)

    def delete_configuration(self, configuration_id):

        return self.client.delete_configuration(configuration_id)

    def toggle_configuration(self, configuration_id, enabled):
        
        return self.client.toggle_configuration(configuration_id, enabled)

    def get_analysis_status(self, user_id: str):
        
        return self.client.get_analysis_status(user_id)
    
    def toggle_analysis(self, user_id: str, enabled: bool):
        
        return self.client.toggle_analysis(user_id, enabled)

    def get_signals(
        self,
        user_id: str,
        symbol: str | None = None,
        strategy: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ):
        
        return self.client.get_signals(
            user_id=user_id,
            symbol=symbol,
            strategy=strategy,
            page=page,
            page_size=page_size,
        )

    def refresh_registries(self):
        
        return self.client.refresh_registries()

    def get_strategies(self):
        
        return self.client.get_strategies()

    def get_symbols(self, search: str | None = None):

        return self.client.get_symbols(search=search or None)

    def get_timeframes(self):

        return self.client.get_timeframes()
