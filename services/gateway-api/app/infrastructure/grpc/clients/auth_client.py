import grpc
from app.config.settings import AUTH_SERVICE_HOST, AUTH_SERVICE_PORT, AUTH_SERVICE_SECURE, AUTH_SERVICE_CERT
from app.infrastructure.protos.generated import auth_pb2, auth_pb2_grpc

class AuthClient:
    def __init__(self):
        address = f"{AUTH_SERVICE_HOST}:{AUTH_SERVICE_PORT}"

        if AUTH_SERVICE_SECURE:
            with open(AUTH_SERVICE_CERT, "rb") as f:
                credentials = grpc.ssl_channel_credentials(f.read())
            self.channel = grpc.secure_channel(address, credentials)
        else:
            self.channel = grpc.insecure_channel(address)

        self.stub = auth_pb2_grpc.AuthServiceStub(self.channel)

    def register(self, email: str, password: str):
        return self.stub.Register(
            auth_pb2.RegisterRequest(
                email=email,
                password=password
            )
        )

    def login(self, email: str, password: str):
        return self.stub.Login(
            auth_pb2.LoginRequest(
                email=email,
                password=password
            )
        )

    def validate(self, token: str):
        return self.stub.Validate(
            auth_pb2.ValidateRequest(token=token)
        )

    def update_telegram(self, user_id: str, token: str, chat_id: str):
        return self.stub.UpdateTelegram(
            auth_pb2.UpdateTelegramRequest(
                user_id=user_id,
                telegram_token=token,
                telegram_chat_id=chat_id
            )
        )
