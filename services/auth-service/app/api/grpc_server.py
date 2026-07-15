import grpc, logging
from app.infrastructure.protos.generated import auth_pb2, auth_pb2_grpc
from app.application.services.auth_service import AuthService
from app.infrastructure.database.connection import SessionLocal
from app.infrastructure.database.user_repository_impl import UserRepositoryImpl
from app.infrastructure.security.jwt_handler import decode_token
from app.domain.exceptions import UserAlreadyExistsException, InvalidCredentialsException
from app.infrastructure.security.encryption import decrypt

logger = logging.getLogger("auth")

class AuthServiceServicer(auth_pb2_grpc.AuthServiceServicer):
    def Register(self, request, context):
        request_id = _get_request_id(context)
        logger.info(
            "register_called",
            extra={
                "request_id": request_id,
                "service": "auth",
            }
        )

        try:
            with SessionLocal() as db:
                repo = UserRepositoryImpl(db)
                service = AuthService(repo)

                result = service.register(
                    email=request.email,
                    password=request.password
                )

                return auth_pb2.AuthResponse(
                    user_id=result.user_id,
                    token=result.token
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
        request_id = _get_request_id(context)
        logger.info(
            "login_called",
            extra={
                "request_id": request_id,
                "service": "auth",
            }
        )

        try:
            with SessionLocal() as db:
                repo = UserRepositoryImpl(db)
                service = AuthService(repo)

                result = service.login(
                    email=request.email,
                    password=request.password
                )

                return auth_pb2.AuthResponse(
                    user_id=result.user_id,
                    token=result.token
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
        request_id = _get_request_id(context)
        logger.info(
            "validate_called",
            extra={
                "request_id": request_id,
                "service": "auth",
            }
        )

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
                    email=user.email,
                    is_active=user.is_active
                )
            
        except Exception as e:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details("Invalid token: " + str(e))

            return auth_pb2.UserResponse()
        
    def UpdateTelegram(self, request, context):
        request_id = _get_request_id(context)
        logger.info(
            "update_telegram_called",
            extra={
                "request_id": request_id,
                "service": "auth",
            }
        )

        try:
            with SessionLocal() as db:
                repo = UserRepositoryImpl(db)
                service = AuthService(repo)

                user = service.update_telegram(
                    user_id=request.user_id,
                    token=request.telegram_token,
                    chat_id=request.telegram_chat_id
                )

                return auth_pb2.UserResponse(
                    user_id=str(user.id),
                    email=user.email,
                    is_active=user.is_active
                )
            
        except InvalidCredentialsException as e:
            context.set_code(grpc.StatusCode.UNAUTHENTICATED)
            context.set_details(str(e))

            return auth_pb2.UserResponse()
        
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error: " + str(e))

            return auth_pb2.UserResponse()
            
    def GetUser(self, request, context):
        request_id = _get_request_id(context)
        logger.info(
            "get_user_called",
            extra={
                "request_id": request_id,
                "service": "auth",
            }
        )
        
        try:
            with SessionLocal() as db:
                repository = UserRepositoryImpl(db)
                user = repository.get_by_id(request.user_id)

                return auth_pb2.UserTelegramResponse(
                    user_id=str(user.id),
                    email=user.email,
                    telegram_token=user.telegram_token or "",
                    telegram_chat_id=user.telegram_chat_id or "",
                )
            
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error: " + str(e))

            return auth_pb2.UserTelegramResponse()
        
    def GetUsers(self, request, context):
        request_id = _get_request_id(context)
        logger.info(
            "get_users_called",
            extra={
                "request_id": request_id,
                "service": "auth",
            }
        )

        try:
            with SessionLocal() as db:
                repo = UserRepositoryImpl(db)
                users = repo.get_all()

                return auth_pb2.GetUsersResponse(
                    users=[
                        auth_pb2.UserTelegramResponse(
                            user_id=str(user.id),
                            email=user.email,
                            telegram_token=decrypt(user.telegram_token) if user.telegram_token else "",
                            telegram_chat_id=decrypt(user.telegram_chat_id) if user.telegram_chat_id else "",
                        )
                        for user in users
                    ]
                )
        
        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details("Internal server error: " + str(e))

            return auth_pb2.GetUsersResponse()
            
def _get_request_id(context):
    metadata = dict(context.invocation_metadata())
    
    return metadata.get("request-id")
