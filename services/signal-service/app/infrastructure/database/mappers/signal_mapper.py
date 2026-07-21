from app.domain.entities.signal import Signal
from app.infrastructure.database.models.signal import SignalModel

class SignalMapper:
    @staticmethod
    def to_model(signal: Signal):
        
        return SignalModel(
            id=signal.id,
            user_id=signal.user_id,
            symbol=signal.symbol,
            strategy=signal.strategy,
            signal=signal.signal,
            trend_timeframe=signal.trend_timeframe,
            context_timeframe=signal.context_timeframe,
            entry_timeframe=signal.entry_timeframe,
            price=signal.price,
            signal_time=signal.signal_time,
            candle_time=signal.candle_time,
            dedup_key=signal.dedup_key,
        )
