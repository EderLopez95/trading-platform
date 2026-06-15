import grpc
from concurrent import futures
from app.infrastructure.protos.generated import auth_pb2, auth_pb2_grpc
from app.application.services.auth_service import AuthService
from app.infrastructure.database.connection import SessionLocal
from app.infrastructure.database.user_repository_impl import UserRepositoryImpl
from app.infrastructure.security.jwt_handler import decode_token
from app.domain.exceptions import UserAlreadyExistsException, InvalidCredentialsException
from app.config.settings import ENV, GRPC_PORT, GRPC_SSL_CERT, GRPC_SSL_KEY
from app.domain.exceptions import TLSMissingCertKeyException

class AuthServiceServicer(auth_pb2_grpc.AuthServiceServicer):
    def Register(self, request, context):
        with SessionLocal() as db:
            repo = UserRepositoryImpl(db)
            service = AuthService(repo)

            try:
                result = service.register(
                    email=request.email,
                    password=request.password
                )
                return auth_pb2.AuthResponse(
                    user_id=result["user_id"],
                    token=result["token"]
                )
            except UserAlreadyExistsException as e:
                context.set_code(grpc.StatusCode.ALREADY_EXISTS)
                context.set_details(str(e))
                return auth_pb2.AuthResponse()
            except Exception as e:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error: " + str(e))
                return auth_pb2.AuthResponse()
            
    def Login(self, request, context):
        with SessionLocal() as db:
            repo = UserRepositoryImpl(db)
            service = AuthService(repo)

            try:
                result = service.login(
                    email=request.email,
                    password=request.password
                )
                return auth_pb2.AuthResponse(
                    user_id=result["user_id"],
                    token=result["token"]
                )
            except InvalidCredentialsException as e:
                context.set_code(grpc.StatusCode.UNAUTHENTICATED)
                context.set_details(str(e))
                return auth_pb2.AuthResponse()
            except Exception as e:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error: " + str(e))
                return auth_pb2.AuthResponse()
            
    def Validate(self, request, context):
        try:
            payload = decode_token(request.token)
            user_id = payload["sub"]

            with SessionLocal() as db:
                repo = UserRepositoryImpl(db)
                user = repo.get_by_id(user_id)

                if not user:
                    context.set_code(grpc.StatusCode.UNAUTHENTICATED)
                    context.set_details("User not found")
                    return auth_pb2.UserResponse()

                return auth_pb2.UserResponse(
                    user_id=str(user.id),
                    email=user.email
                )
        except Exception as e:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("Invalid token: " + str(e))
            return auth_pb2.UserResponse()
        
    def UpdateTelegram(self, request, context):
        with SessionLocal() as db:
            repo = UserRepositoryImpl(db)
            service = AuthService(repo)

            try:
                user = service.update_telegram(
                    user_id=request.user_id,
                    token=request.telegram_token,
                    chat_id=request.telegram_chat_id
                )
                return auth_pb2.UserResponse(
                    user_id=str(user.id),
                    email=user.email
                )
            except InvalidCredentialsException as e:
                context.set_code(grpc.StatusCode.UNAUTHENTICATED)
                context.set_details(str(e))
                return auth_pb2.UserResponse()
            except Exception as e:
                context.set_code(grpc.StatusCode.INTERNAL)
                context.set_details("Internal server error: " + str(e))
                return auth_pb2.UserResponse()
            
def create_server():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )
    auth_pb2_grpc.add_AuthServiceServicer_to_server(
        AuthServiceServicer(),
        server
    )
    address = f"[::]:{GRPC_PORT}"
    
    if ENV == "prod":
        _add_secure_port(server, address)
        print(f"gRPC Secure server running on {address}")
    else:
        server.add_insecure_port(address)
        print(f"gRPC Insecure server running on {address}")
    return server

def _add_secure_port(server, address):
    if not GRPC_SSL_CERT or not GRPC_SSL_KEY:
        raise TLSMissingCertKeyException("GRPC_SSL_CERT / GRPC_SSL_KEY")

    with open(GRPC_SSL_CERT, "rb") as f:
        certificate_chain = f.read()
    with open(GRPC_SSL_KEY, "rb") as f:
        private_key = f.read()

    server_credentials = grpc.ssl_server_credentials(
        [(private_key, certificate_chain)]
    )
    server.add_secure_port(address, server_credentials)
