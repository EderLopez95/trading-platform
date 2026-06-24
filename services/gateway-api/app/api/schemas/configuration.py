from pydantic import BaseModel

class CreateConfigurationRequest(BaseModel):
    symbols: list[str]
    strategies: list[str]
    trend_timeframe: str
    context_timeframe: str | None = None
    entry_timeframe: str

class ToggleConfigurationRequest(BaseModel):
    enabled: bool
