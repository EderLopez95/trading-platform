from fastapi import APIRouter, Depends, Request, BackgroundTasks
from fastapi.security import HTTPAuthorizationCredentials
from app.application.services.auth_service import AuthService
from app.api.dependencies.auth import get_current_user, security
from app.api.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    UpdateTelegramRequest,
    AuthResponse,
    UserResponse,
    CurrentUserResponse,
    TelegramSettingsResponse
)
from app.api.background import refresh_registries_safe
from app.core.security.rate_limiter import RateLimiter
from app.config.settings import LOGIN_RATE_LIMIT_MAX, LOGIN_RATE_LIMIT_WINDOW
from app.infrastructure.grpc.clients.providers import get_auth_client

router = APIRouter()
login_rate_limiter = RateLimiter(LOGIN_RATE_LIMIT_MAX, LOGIN_RATE_LIMIT_WINDOW)

def get_service():

    return AuthService(get_auth_client())

@router.post("/register", response_model=AuthResponse)
def register(
    request: Request,
    data: RegisterRequest,
    background_tasks: BackgroundTasks,
    service: AuthService = Depends(get_service)
):
    request_id = request.state.request_id
    res = service.register(data.email, data.password, request_id)

    if res:
        background_tasks.add_task(refresh_registries_safe)

    return AuthResponse(
        user_id=res.user_id,
        token=res.token
    )

@router.post("/login", response_model=AuthResponse)
def login(
    request: Request,
    data: LoginRequest,
    service: AuthService = Depends(get_service),
    _: None = Depends(login_rate_limiter),
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
    background_tasks: BackgroundTasks,
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

    if res:
        background_tasks.add_task(refresh_registries_safe)

    return UserResponse(user_id=res.user_id)

@router.get("/me", response_model=CurrentUserResponse)
def me(
    _user=Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security),
    service: AuthService = Depends(get_service),
):
    res = service.validate(credentials.credentials)

    return CurrentUserResponse(
        id=res.user_id,
        email=res.email,
        is_active=res.is_active
    )

@router.get("/telegram", response_model=TelegramSettingsResponse)
def get_telegram(
    request: Request,
    user=Depends(get_current_user),
    service: AuthService = Depends(get_service),
):
    request_id = request.state.request_id
    res = service.get_user(user.user_id, request_id)

    return TelegramSettingsResponse(
        telegram_token=res.telegram_token,
        telegram_chat_id=res.telegram_chat_id,
    )
