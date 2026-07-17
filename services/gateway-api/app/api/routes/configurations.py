from fastapi import APIRouter, Depends
from app.api.dependencies.auth import get_current_user
from app.infrastructure.grpc.clients.signal_client import SignalClient
from app.application.services.signal_service import SignalService
from app.api.schemas.configuration import CreateConfigurationRequest, ToggleConfigurationRequest
from app.api.mappers.configuration_mapper import ConfigurationMapper

router = APIRouter()

def get_service():

    return SignalService(SignalClient())

@router.get("")
def get_configurations(
    user=Depends(get_current_user),
    service: SignalService = Depends(get_service)
):
    result = service.get_configurations(user.user_id)

    return {
        "configurations": [
            ConfigurationMapper.to_dict(c)
            for c in result.configurations
        ]
    }

@router.post("")
def create_configuration(
    data: CreateConfigurationRequest,
    user=Depends(get_current_user),
    service: SignalService = Depends(get_service)
):
    result = service.create_configuration(user.user_id, data)
    
    if result:
        service.refresh_registries()

    return ConfigurationMapper.to_dict(result.configuration)

@router.delete("/{configuration_id}")
def delete_configuration(
    configuration_id: str,
    service: SignalService = Depends(get_service)
):
    service.delete_configuration(configuration_id)
    service.refresh_registries()

    return {"message": "Configuration deleted successfully"}

@router.patch("/{configuration_id}/status")
def toggle_configuration(
    configuration_id: str,
    data: ToggleConfigurationRequest,
    service: SignalService = Depends(get_service)
):
    result = service.toggle_configuration(configuration_id, data.enabled)
    
    if result:
        service.refresh_registries()

    return ConfigurationMapper.to_dict(result.configuration)
