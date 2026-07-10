class NotificationService:
    def __init__(self, provider):
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
