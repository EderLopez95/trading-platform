from app.infrastructure.database.repositories.configuration_repository import ConfigurationRepository
from app.infrastructure.scheduler.configuration_registry import ConfigurationRegistry

class LoadRegistryUseCase:
    def __init__(self, repository: ConfigurationRepository, registry: ConfigurationRegistry):
        self.repository = repository
        self.registry = registry

    def execute(self):
        configurations = self.repository.get_enabled()
        self.registry.load(configurations)

        return len(configurations)
