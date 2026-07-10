from app.infrastructure.grpc.clients.auth_client import AuthClient
from app.domain.entities.user_profile import UserProfile

class UserProfileService:
    def __init__(self, auth_client: AuthClient):
        self.auth_client = auth_client

    def get_user(self, user_id: str) -> UserProfile:
        user = self.auth_client.get_user(user_id)

        return UserProfile(
            user_id=user.user_id,
            email=user.email,
            telegram_token=user.telegram_token,
            telegram_chat_id=user.telegram_chat_id,
        )
