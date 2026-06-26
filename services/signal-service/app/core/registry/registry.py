from app.infrastructure.database.connection import SessionLocal
from app.infrastructure.scheduler.registry_container import configuration_registry, user_registry
from app.infrastructure.database.repositories.configuration_repository import ConfigurationRepositoryImpl
from app.infrastructure.database.repositories.user_settings_repository import UserSettingsRepositoryImpl
from app.application.services.configuration_registry_service import ConfigurationRegistryService
from app.application.services.user_registry_service import UserRegistryService
from app.infrastructure.scheduler.engine_runner import start_engine

def load_registries():
    with SessionLocal() as db:
        configuration_repository = ConfigurationRepositoryImpl(db)
        user_repository = UserSettingsRepositoryImpl(db)
        configs_loaded = (
            ConfigurationRegistryService(
                configuration_repository,
                configuration_registry,
            ).load()
        )
        users_loaded = (
            UserRegistryService(
                user_repository,
                user_registry,
            ).load()
        )
        print(f"Loaded configurations: {configs_loaded}", flush=True)
        print(f"Loaded users: {users_loaded}", flush=True)
        
    start_engine()
