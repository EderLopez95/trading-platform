from fastapi import APIRouter, Depends
from app.api.dependencies.auth import get_current_user
from app.infrastructure.grpc.clients.signal_client import SignalClient
from app.application.services.signal_service import SignalService
from app.api.schemas.configuration import CreateConfigurationRequest, ToggleConfigurationRequest

router = APIRouter()

def get_service():

    return SignalService(SignalClient())

@router.get("")
def get_configurations(
    user=Depends(get_current_user),
    service: SignalService = Depends(get_service)
):
    
    return service.get_configurations(user.user_id)

@router.post("")
def create_configuration(
    data: CreateConfigurationRequest,
    user=Depends(get_current_user),
    service: SignalService = Depends(get_service)
):
    
    return service.create_configuration(user.user_id, data)

@router.delete("/{configuration_id}")
def delete_configuration(
    configuration_id: str,
    service: SignalService = Depends(get_service)
):
    
    return service.delete_configuration(configuration_id)

@router.patch(
    "/{configuration_id}/status"
)
def toggle_configuration(
    configuration_id: str,
    data: ToggleConfigurationRequest,
    service: SignalService = Depends(get_service)
):
    
    return service.toggle_configuration(configuration_id, data.enabled)
