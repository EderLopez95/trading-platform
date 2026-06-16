from fastapi import APIRouter, Depends, Request
from app.infrastructure.grpc.clients.auth_client import AuthClient
from app.application.services.auth_service import AuthService
from app.api.dependencies.auth import get_current_user
from app.api.schemas.auth import RegisterRequest, LoginRequest, UpdateTelegramRequest, AuthResponse, UserResponse

router = APIRouter()

def get_service():
    return AuthService(AuthClient())

@router.post("/register", response_model=AuthResponse)
def register(
    request: Request,
    data: RegisterRequest,
    service: AuthService = Depends(get_service)
):
    request_id = request.state.request_id
    res = service.register(data.email, data.password, request_id)
    return AuthResponse(
        user_id=res.user_id,
        token=res.token
    )

@router.post("/login", response_model=AuthResponse)
def login(
    request: Request,
    data: LoginRequest,
    service: AuthService = Depends(get_service)
):
    request_id = request.state.request_id
    res = service.login(data.email, data.password, request_id)
    return AuthResponse(
        user_id=res.user_id,
        token=res.token
    )

@router.put("/telegram", response_model=UserResponse)
def update_telegram(
    request: Request,
    data: UpdateTelegramRequest,
    user=Depends(get_current_user),
    service: AuthService = Depends(get_service),
):
    request_id = request.state.request_id
    request.state.user_id = user.user_id
    res = service.update_telegram(
        user.user_id,
        data.telegram_token,
        data.telegram_chat_id,
        request_id
    )
    return UserResponse(user_id=res.user_id)
