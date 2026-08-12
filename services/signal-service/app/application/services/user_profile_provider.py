import time, logging
from app.domain.entities.user_profile import UserProfile
from app.infrastructure.grpc.clients.auth_client import AuthClient
from app.infrastructure.scheduler.user_profile_registry import UserProfileRegistry

logger = logging.getLogger("signal")

class UserProfileProvider:
    def __init__(
        self,
        auth_client: AuthClient,
        registry: UserProfileRegistry,
        ttl_seconds: int = 300,
    ):
        self._auth_client = auth_client
        self._registry = registry
        self._ttl_seconds = ttl_seconds
        self._fetched_at = {}

    def get(self, user_id: str):
        now = time.time()

        if now - self._fetched_at.get(user_id, 0) < self._ttl_seconds:
            
            return self._registry.get(user_id)

        try:
            user = self._auth_client.get_user(user_id)

            self._registry.update(
                UserProfile(
                    user_id=user.user_id,
                    email=user.email,
                    telegram_token=user.telegram_token,
                    telegram_chat_id=user.telegram_chat_id,
                )
            )
            self._fetched_at[user_id] = now

        except Exception as e:
            logger.error(
                "profile_refresh_failed",
                extra={
                    "user_id": user_id,
                    "error": str(e),
                }
            )

        return self._registry.get(user_id)
