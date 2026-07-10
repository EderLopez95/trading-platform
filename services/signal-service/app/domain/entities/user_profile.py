from dataclasses import dataclass

@dataclass
class UserProfile:
    user_id: str
    email: str
    telegram_token: str | None
    telegram_chat_id: str | None
