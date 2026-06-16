import grpc
from app.config.settings import AUTH_SERVICE_HOST, AUTH_SERVICE_PORT, AUTH_SERVICE_SECURE, AUTH_SERVICE_CERT
from app.infrastructure.protos.generated import auth_pb2, auth_pb2_grpc
from app.infrastructure.grpc.error_mapper import map_grpc_error

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

    def register(self, email: str, password: str, request_id: str | None = None):
        try:
            metadata = []
            
            if request_id:
                metadata.append(("request-id", request_id))

            return self.stub.Register(
                auth_pb2.RegisterRequest(email=email, password=password),
                metadata=metadata
            )
        except grpc.RpcError as e:
            map_grpc_error(e)

    def login(self, email: str, password: str, request_id=None):
        try:
            metadata = [("request-id", request_id)] if request_id else []
            return self.stub.Login(
                auth_pb2.LoginRequest(email=email, password=password),
                metadata=metadata
            )
        except grpc.RpcError as e:
            map_grpc_error(e)

    def validate(self, token: str, request_id=None):
        try:
            metadata = [("request-id", request_id)] if request_id else []
            return self.stub.Validate(
                auth_pb2.ValidateRequest(token=token),
                metadata=metadata
            )
        except grpc.RpcError as e:
            map_grpc_error(e)

    def update_telegram(self, user_id: str, token: str, chat_id: str, request_id=None):
        try:
            metadata = [("request-id", request_id)] if request_id else []
            
            if user_id:
                metadata.append(("user-id", str(user_id)))

            return self.stub.UpdateTelegram(
                auth_pb2.UpdateTelegramRequest(
                    user_id=user_id,
                    telegram_token=token,
                    telegram_chat_id=chat_id,
                ),
                metadata=metadata
            )
        except grpc.RpcError as e:
            map_grpc_error(e)
