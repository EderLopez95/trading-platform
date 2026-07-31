from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from datetime import datetime
from app.domain.enums.enums import SignalType, Timeframe

class TimeframesModel(BaseModel):
    trend: Timeframe
    context: Optional[Timeframe] = None
    entry: Timeframe

class ConfigurationModel(BaseModel):
    id: UUID | None = None
    user_id: UUID
    symbols: list[str] = Field(min_length=1)
    strategies: list[str] = Field(min_length=1)
    params: dict | None = None
    timeframes: TimeframesModel
    enabled: bool = True
    created_at: datetime | None = None

class SignalModel(BaseModel):
    id: UUID | None = None
    user_id: UUID
    symbol: str
    strategy: str
    signal: SignalType
    trend_timeframe: Timeframe
    context_timeframe: Timeframe | None = None
    entry_timeframe: Timeframe
    price: float | None = None
    signal_time: datetime
    candle_time: datetime
    dedup_key: str
    created_at: datetime | None = None
