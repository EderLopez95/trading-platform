from app.infrastructure.protos.generated import signal_pb2

class SignalMapper:
    @staticmethod
    def to_proto(signal):
        
        return signal_pb2.SignalDto(
            id=str(signal.id),
            symbol=signal.symbol,
            strategy=signal.strategy,
            signal=signal.signal,
            trend_timeframe=signal.trend_timeframe,
            context_timeframe=signal.context_timeframe or "",
            entry_timeframe=signal.entry_timeframe,
            price=float(signal.price),
            signal_time=signal.signal_time.isoformat(),
        )
