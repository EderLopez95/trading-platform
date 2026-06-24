from app.infrastructure.protos.generated import signal_pb2

class ConfigurationGrpcMapper:
    @staticmethod
    def to_proto(configuration):
        return signal_pb2.ConfigurationDto(
            id=configuration.id,
            user_id=configuration.user_id,
            symbols=configuration.symbols,
            strategies=configuration.strategies,
            trend_timeframe=configuration.trend_timeframe,
            context_timeframe=(configuration.context_timeframe or ""),
            entry_timeframe=configuration.entry_timeframe,
            enabled=configuration.enabled,
        )
