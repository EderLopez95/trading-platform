from app.domain.entities.user_profile import UserProfile
from app.infrastructure.grpc.clients.auth_client import AuthClient
from app.infrastructure.scheduler.user_profile_registry import UserProfileRegistry

class UserProfileRegistryService:
    def __init__(self, auth_client: AuthClient, registry: UserProfileRegistry):
        self.auth_client = auth_client
        self.registry = registry

    def load(self):
        response = self.auth_client.get_users()
        profiles = []

        for user in response.users:
            profiles.append(
                UserProfile(
                    user_id=user.user_id,
                    email=user.email,
                    telegram_token=user.telegram_token,
                    telegram_chat_id=user.telegram_chat_id,
                )
            )

        self.registry.load(profiles)

        return len(profiles)
