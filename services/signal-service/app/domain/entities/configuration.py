from dataclasses import dataclass
from datetime import datetime

@dataclass
class Configuration:
    id: str
    user_id: str
    symbols: list[str]
    strategies: list[str]
    params: dict | None
    trend_timeframe: str
    context_timeframe: str | None
    entry_timeframe: str
    enabled: bool
    created_at: datetime
