import uuid
from datetime import datetime
from sqlalchemy import String, TIMESTAMP, Numeric, Index, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.models.base import Base

class SignalModel(Base):
    __tablename__ = "signals"
    __table_args__ = (
        Index("idx_signals_user_id", "user_id"),
        Index("idx_signals_user_time", "user_id", "signal_time"),
        Index("idx_signals_symbol", "symbol"),
        Index("idx_signals_time", "signal_time"),
        Index("uq_signals_dedup", "user_id", "dedup_key", "candle_time", unique=True),
        {"schema": "signals"}
    )

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    symbol: Mapped[str] = mapped_column(String, nullable=False)
    strategy: Mapped[str] = mapped_column(String, nullable=False)
    signal: Mapped[str] = mapped_column(String, nullable=False)
    trend_timeframe: Mapped[str] = mapped_column(String(10), nullable=False)
    context_timeframe: Mapped[str | None] = mapped_column(String(10))
    entry_timeframe: Mapped[str] = mapped_column(String(10), nullable=False)
    price: Mapped[float | None] = mapped_column(Numeric, nullable=True)
    signal_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    candle_time: Mapped[datetime] = mapped_column(TIMESTAMP, nullable=False)
    dedup_key: Mapped[str] = mapped_column(String, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
