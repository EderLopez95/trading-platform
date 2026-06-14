import grpc
from concurrent import futures
from app.infrastructure.protos.generated import auth_pb2, auth_pb2_grpc
from app.application.services.auth_service import AuthService
from app.infrastructure.database.connection import SessionLocal
from app.infrastructure.database.user_repository_impl import UserRepositoryImpl
from app.infrastructure.security.jwt_handler import decode_token
from app.domain.exceptions import UserAlreadyExistsException, InvalidCredentialsException

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
        
def create_server():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )
    auth_pb2_grpc.add_AuthServiceServicer_to_server(
        AuthServiceServicer(),
        server
    )
    server.add_insecure_port("[::]:5051")
    return server
