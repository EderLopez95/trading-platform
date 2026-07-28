from app.application.services.configuration_registry_service import ConfigurationRegistryService
from app.application.services.user_registry_service import UserRegistryService
from app.application.services.user_profile_registry_service import UserProfileRegistryService

class RegistryRefreshService:
    def __init__(
        self,
        configuration_service: ConfigurationRegistryService,
        user_service: UserRegistryService,
        profile_service: UserProfileRegistryService,
    ):
        self.configuration_service = configuration_service
        self.user_service = user_service
        self.profile_service = profile_service

    def refresh(self):
        users = self.user_service.load()
        profiles = self.profile_service.load()
        configurations = self.configuration_service.load()

        return {
            "users": users,
            "configurations": configurations,
            "profiles": profiles,
        }
