from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

@dataclass
class Signal:
    id: str
    user_id: str
    symbol: str
    strategy: str
    signal: str
    trend_timeframe: str
    context_timeframe: str | None
    entry_timeframe: str
    price: Decimal | None
    signal_time: datetime
    candle_time: datetime
    dedup_key: str
    created_at: datetime | None = None
