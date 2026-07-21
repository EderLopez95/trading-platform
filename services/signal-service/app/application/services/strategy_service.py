from app.infrastructure.scheduler.strategy_container import strategy_registry

class StrategyService:
    def get_all(self):

        return [
            {
                "id": name,
                "name": name,
            }
            for name in strategy_registry.get_names()
        ]

    def exists(self, strategy_name: str):

        return (
            strategy_registry.get(strategy_name)
            is not None
        )
