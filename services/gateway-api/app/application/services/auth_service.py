from app.domain.ports.auth_port import AuthPort

class AuthService:
    def __init__(self, auth_client: AuthPort):
        self.auth_client = auth_client

    def register(self, email: str, password: str):
        return self.auth_client.register(email, password)

    def login(self, email: str, password: str):
        return self.auth_client.login(email, password)

    def validate(self, token: str):
        return self.auth_client.validate(token)

    def update_telegram(self, user_id: str, token: str, chat_id: str):
        return self.auth_client.update_telegram(user_id, token, chat_id)
