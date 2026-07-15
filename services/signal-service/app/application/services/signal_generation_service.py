import uuid
from datetime import datetime, timezone
from app.domain.entities.signal import Signal
from app.domain.enums.enums import SignalType
from app.domain.utils.signal_dedup import build_dedup_key

class SignalGenerationService:
    def __init__(self, repository):
        self.repository = repository

    def generate(
        self,
        configuration,
        symbol: str,
        strategy: str,
        result,
        candle_time,
        price: float,
    ):

        if result.signal == SignalType.NONE:
            return None

        dedup_key = (
            build_dedup_key(
                symbol=symbol,
                strategy=strategy,
                signal=result.signal.value,
                timeframe=configuration.entry_timeframe,
            )
        )

        if self.repository.exists(
            user_id=configuration.user_id,
            dedup_key=dedup_key,
            candle_time=candle_time,
        ):
            
            return None

        signal = Signal(
            id=str(uuid.uuid4()),
            user_id=configuration.user_id,
            symbol=symbol,
            strategy=strategy,
            signal=result.signal.value,
            trend_timeframe=configuration.trend_timeframe,
            context_timeframe=configuration.context_timeframe,
            entry_timeframe=configuration.entry_timeframe,
            price=price,
            signal_time=datetime.now(timezone.utc),
            candle_time=candle_time,
            dedup_key=dedup_key,
        )

        return self.repository.create(signal)
