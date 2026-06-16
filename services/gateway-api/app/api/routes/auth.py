from fastapi import APIRouter, Depends
from app.infrastructure.grpc.clients.auth_client import AuthClient
from app.application.services.auth_service import AuthService
from app.api.dependencies.auth import get_current_user

router = APIRouter()

def get_service():
    return AuthService(AuthClient())

@router.post("/register")
def register(data: dict, service: AuthService = Depends(get_service)):
    res = service.register(data["email"], data["password"])
    return {
        "user_id": res.user_id,
        "token": res.token,
    }

@router.post("/login")
def login(data: dict, service: AuthService = Depends(get_service)):
    res = service.login(data["email"], data["password"])
    return {
        "user_id": res.user_id,
        "token": res.token,
    }

@router.put("/telegram")
def update_telegram(
    data: dict,
    user=Depends(get_current_user),
    service: AuthService = Depends(get_service),
):
    res = service.update_telegram(
        user.user_id,
        data["telegram_token"],
        data["telegram_chat_id"],
    )
    return {
        "user_id": res.user_id,
    }
