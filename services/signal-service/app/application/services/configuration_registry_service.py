from app.domain.repositories.configuration_repository import ConfigurationRepository
from app.infrastructure.scheduler.configuration_registry import ConfigurationRegistry
from app.infrastructure.scheduler.registry_container import user_registry

class ConfigurationRegistryService:
    def __init__(self, repository: ConfigurationRepository, registry: ConfigurationRegistry):
        self.repository = repository
        self.registry = registry

    def load(self):
        configurations = self.repository.get_all()
        total = len(configurations)
        active_configurations = [
            configuration
            for configuration in configurations

            if user_registry.is_analysis_enabled(configuration.user_id) and configuration.enabled
        ]
        self.registry.load(active_configurations)

        return {
            "loaded": len(active_configurations),
            "excluded": (total - len(active_configurations)),
        }
