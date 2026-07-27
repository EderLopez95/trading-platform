from pydantic import BaseModel

class SignalResponse(BaseModel):
    id: str
    symbol: str
    strategy: str
    signal: str
    trend_timeframe: str
    context_timeframe: str
    entry_timeframe: str
    price: float
    signal_time: str

class SignalsResponse(BaseModel):
    signals: list[SignalResponse]
    page: int
    page_size: int
    total: int

class StrategyResponse(BaseModel):
    id: str
    name: str

class StrategiesResponse(BaseModel):
    strategies: list[StrategyResponse]

class SymbolResponse(BaseModel):
    symbol: str

class SymbolsResponse(BaseModel):
    symbols: list[SymbolResponse]

class TimeframeResponse(BaseModel):
    timeframe: str

class TimeframesResponse(BaseModel):
    timeframes: list[TimeframeResponse]
