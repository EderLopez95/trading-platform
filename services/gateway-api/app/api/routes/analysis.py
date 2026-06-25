from fastapi import APIRouter, Depends
from app.api.dependencies.auth import get_current_user
from app.infrastructure.grpc.clients.signal_client import SignalClient
from app.application.services.signal_service import SignalService
from app.api.schemas.analysis import AnalysisStatusResponse, ToggleAnalysisRequest

router = APIRouter()

def get_service():

    return SignalService(SignalClient())

@router.get("/status", response_model=AnalysisStatusResponse)
def get_analysis_status(
    user=Depends(get_current_user),
    service: SignalService = Depends(get_service),
):
    result = service.get_analysis_status(user.user_id)

    return AnalysisStatusResponse(enabled=result.enabled)

@router.patch("/status", response_model=AnalysisStatusResponse)
def toggle_analysis(
    data: ToggleAnalysisRequest,
    user=Depends(get_current_user),
    service: SignalService = Depends(get_service),
):
    result = (
        service.toggle_analysis(
            user.user_id,
            data.enabled,
        )
    )

    return AnalysisStatusResponse(enabled=result.enabled)
