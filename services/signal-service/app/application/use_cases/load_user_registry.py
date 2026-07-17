from app.infrastructure.database.repositories.user_settings_repository import UserSettingsRepositoryImpl
from app.infrastructure.scheduler.configuration_registry import ConfigurationRegistry

class LoadUserRegistryUseCase:
    def __init__(self, repository: UserSettingsRepositoryImpl, registry: ConfigurationRegistry):
        self.repository = repository
        self.registry = registry

    def execute(self):
        settings = self.repository.get_users()
        self.registry.load(settings)

        return len(settings)
