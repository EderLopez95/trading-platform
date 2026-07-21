from app.infrastructure.grpc.clients.market_data_client import MarketDataClient

class SymbolService:
    def __init__(self, client: MarketDataClient):
        self.client = client

    def get_all(self, search: str | None = None):
        response = (self.client.get_symbols(search=search or None))

        return [
            symbol.symbol
            for symbol in response.symbols
        ]
