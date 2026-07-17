from app.infrastructure.scheduler.user_registry import UserRegistry
from app.infrastructure.database.repositories.user_settings_repository import UserSettingsRepositoryImpl

class UserRegistryService:
    def __init__(self, repository: UserSettingsRepositoryImpl, registry: UserRegistry):
        self.repository = repository
        self.registry = registry

    def load(self):
        response = self.repository.get_users()
        self.registry.load(response)

        return len(response)
