from app.infrastructure.notifications.telegram_adapter import TelegramAdapter

class NotificationService:
    def __init__(self, provider: TelegramAdapter):
        self.provider = provider

    def send(
        self,
        token: str,
        chat_id: str,
        message: str,
    ):
        self.provider.send(
            token=token,
            chat_id=chat_id,
            message=message,
        )
