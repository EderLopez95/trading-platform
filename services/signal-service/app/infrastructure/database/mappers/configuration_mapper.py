from app.domain.entities.configuration import Configuration

class ConfigurationMapper:
    @staticmethod
    def to_domain(model):
        return Configuration(
            id=str(model.id),
            user_id=str(model.user_id),
            symbols=model.symbols,
            strategies=model.strategies,
            params=model.params,
            trend_timeframe=model.trend_timeframe,
            context_timeframe=model.context_timeframe,
            entry_timeframe=model.entry_timeframe,
            enabled=model.enabled,
            created_at=model.created_at,
        )
