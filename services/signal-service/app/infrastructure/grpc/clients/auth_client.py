import grpc
from app.config.settings import ENV, AUTH_SERVICE_HOST, AUTH_SERVICE_PORT, SIGNAL_SERVICE_SECURE, TRUSTED_CA_CERT
from app.infrastructure.protos.generated import auth_pb2, auth_pb2_grpc

class AuthClient:
    def __init__(self):
        address = (f"{AUTH_SERVICE_HOST}:{AUTH_SERVICE_PORT}")

        if ENV == "prod" and SIGNAL_SERVICE_SECURE:
            with open(TRUSTED_CA_CERT, "rb") as f:
                credentials = grpc.ssl_channel_credentials(f.read())
            self.channel = grpc.secure_channel(address, credentials)
        else:
            self.channel = grpc.insecure_channel(address)

        self.stub = auth_pb2_grpc.AuthServiceStub(self.channel)

    def get_user(self, user_id: str):

        return self.stub.GetUser(
            auth_pb2.GetUserRequest(
                user_id=user_id,
            )
        )
