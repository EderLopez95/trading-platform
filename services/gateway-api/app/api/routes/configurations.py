from fastapi import APIRouter, Depends, BackgroundTasks
from app.api.dependencies.auth import get_current_user
from app.application.services.signal_service import SignalService
from app.api.schemas.configuration import CreateConfigurationRequest, ToggleConfigurationRequest
from app.api.mappers.configuration_mapper import ConfigurationMapper
from app.api.background import refresh_registries_safe
from app.infrastructure.grpc.clients.providers import get_signal_client

router = APIRouter()

def get_service():

    return SignalService(get_signal_client())

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
    background_tasks: BackgroundTasks,
    user=Depends(get_current_user),
    service: SignalService = Depends(get_service)
):
    result = service.create_configuration(user.user_id, data)
    
    if result:
        background_tasks.add_task(refresh_registries_safe)

    return ConfigurationMapper.to_dict(result.configuration)

@router.delete("/{configuration_id}")
def delete_configuration(
    configuration_id: str,
    background_tasks: BackgroundTasks,
    service: SignalService = Depends(get_service)
):
    result = service.delete_configuration(configuration_id)

    if result:
        background_tasks.add_task(refresh_registries_safe)

    return {"message": "Configuration deleted successfully"}

@router.patch("/{configuration_id}/status")
def toggle_configuration(
    configuration_id: str,
    data: ToggleConfigurationRequest,
    background_tasks: BackgroundTasks,
    service: SignalService = Depends(get_service)
):
    result = service.toggle_configuration(configuration_id, data.enabled)
    
    if result:
        background_tasks.add_task(refresh_registries_safe)

    return ConfigurationMapper.to_dict(result.configuration)

@router.patch("/{configuration_id}")
def update_configuration(
    configuration_id: str,
    data: CreateConfigurationRequest,
    background_tasks: BackgroundTasks,
    service: SignalService = Depends(get_service)
):
    result = service.update_configuration(configuration_id, data)

    if result:
        background_tasks.add_task(refresh_registries_safe)

    return ConfigurationMapper.to_dict(result.configuration)
