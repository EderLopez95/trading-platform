class ConfigurationMapper:
    @staticmethod
    def to_dict(configuration):
        return {
            "id": configuration.id,
            "user_id": configuration.user_id,
            "symbols": list(configuration.symbols),
            "strategies": list(configuration.strategies),
            "trend_timeframe": configuration.trend_timeframe,
            "context_timeframe": configuration.context_timeframe or None,
            "entry_timeframe": configuration.entry_timeframe,
            "enabled": configuration.enabled,
        }
