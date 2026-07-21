from app.infrastructure.mt5.mt5_adapter import MT5Adapter

class SymbolService:
    def __init__(self, market_adapter: MT5Adapter):
        self.market_adapter = market_adapter

    def get_all(self, search: str | None = None):
        
        return self.market_adapter.get_symbols(search)
