import uuid
from datetime import datetime
from sqlalchemy import Boolean, String, TIMESTAMP, text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from app.infrastructure.database.models.base import Base

class ConfigurationModel(Base):
    __tablename__ = "configurations"
    __table_args__ = {"schema": "signals"}

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), nullable=False)
    symbols: Mapped[list] = mapped_column(JSONB, nullable=False)
    strategies: Mapped[list] = mapped_column(JSONB, nullable=False)
    params: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    trend_timeframe: Mapped[str] = mapped_column(String(10), nullable=False)
    context_timeframe: Mapped[str | None] = mapped_column(String(10))
    entry_timeframe: Mapped[str] = mapped_column(String(10), nullable=False)
    enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
