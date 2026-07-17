from fastapi import APIRouter, Depends, Query
from app.api.dependencies.auth import get_current_user
from app.infrastructure.grpc.clients.signal_client import SignalClient
from app.application.services.signal_service import SignalService

router = APIRouter()

def get_service():

    return SignalService(SignalClient())

@router.get("/signals")
def get_signals(
    symbol: str | None = Query(default=None),
    strategy: str | None = Query(default=None),
    page: int = Query(default=1),
    page_size: int = Query(default=20),
    current_user=Depends(get_current_user),
    service: SignalService = Depends(get_service)
):
    response = (
        service.get_signals(
            user_id=current_user.user_id,
            symbol=symbol,
            strategy=strategy,
            page=page,
            page_size=page_size,
        )
    )

    return response
