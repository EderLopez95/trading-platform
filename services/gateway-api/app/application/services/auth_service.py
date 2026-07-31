from app.domain.ports.auth_port import AuthPort

class AuthService:
    def __init__(self, auth_client: AuthPort):
        self.auth_client = auth_client

    def register(self, email: str, password: str, request_id=None):

        return self.auth_client.register(email, password, request_id)

    def login(self, email: str, password: str, request_id=None):

        return self.auth_client.login(email, password, request_id)

    def validate(self, token: str, request_id=None):

        return self.auth_client.validate(token, request_id)

    def update_telegram(self, user_id: str, token: str, chat_id: str, request_id=None):
        
        return self.auth_client.update_telegram(user_id, token, chat_id, request_id)

    def get_user(self, user_id: str, request_id=None):

        return self.auth_client.get_user(user_id, request_id)
