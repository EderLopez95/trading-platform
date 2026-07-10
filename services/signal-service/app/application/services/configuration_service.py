import uuid
from app.domain.entities.configuration import Configuration
from app.domain.exceptions.exceptions import ConfigurationNotFoundError
from app.infrastructure.scheduler.registry_container import configuration_registry

class ConfigurationService:
    def __init__(self, repository):
        self.repository = repository

    def get_configurations(self, user_id: str):

        return self.repository.get_by_user(user_id)
    
    def delete_configuration(self, configuration_id: str):
        configuration = self.repository.get_by_id(configuration_id)

        if not configuration:
            raise ConfigurationNotFoundError()
        
        configuration_registry.remove(configuration_id)
        self.repository.delete(configuration_id)

    def toggle_configuration(
        self,
        configuration_id: str,
        enabled: bool,
    ):
        configuration = self.repository.get_by_id(configuration_id)

        if not configuration:
            raise ConfigurationNotFoundError()

        configuration.enabled = enabled
                
        if enabled:
            configuration_registry.register(configuration)
        else:
            configuration_registry.remove(configuration.id)

        return self.repository.update(configuration)

    def create_configuration(
        self,
        user_id: str,
        symbols: list[str],
        strategies: list[str],
        trend_timeframe: str,
        context_timeframe: str | None,
        entry_timeframe: str,
    ):
        configuration = Configuration(
            id=str(uuid.uuid4()),
            user_id=user_id,
            symbols=symbols,
            strategies=strategies,
            params=None,
            trend_timeframe=trend_timeframe,
            context_timeframe=context_timeframe,
            entry_timeframe=entry_timeframe,
            enabled=True,
            created_at=None,
        )

        configuration = self.repository.create(configuration)    
        configuration_registry.register(configuration)
        
        return configuration
