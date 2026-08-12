from fastapi import APIRouter, Depends, BackgroundTasks
from app.api.dependencies.auth import get_current_user
from app.application.services.signal_service import SignalService
from app.api.schemas.analysis import AnalysisStatusResponse, ToggleAnalysisRequest
from app.api.background import refresh_registries_safe
from app.infrastructure.grpc.clients.providers import get_signal_client

router = APIRouter()

def get_service():

    return SignalService(get_signal_client())

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
    background_tasks: BackgroundTasks,
    user=Depends(get_current_user),
    service: SignalService = Depends(get_service),
):
    result = (
        service.toggle_analysis(
            user.user_id,
            data.enabled,
        )
    )
    
    if result:
        background_tasks.add_task(refresh_registries_safe)

    return AnalysisStatusResponse(enabled=result.enabled)
