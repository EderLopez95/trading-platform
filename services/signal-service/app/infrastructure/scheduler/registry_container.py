from app.infrastructure.scheduler.user_registry import UserRegistry
from app.infrastructure.scheduler.configuration_registry import ConfigurationRegistry
from app.infrastructure.scheduler.user_profile_registry import UserProfileRegistry

user_registry = UserRegistry()
configuration_registry = (ConfigurationRegistry())
user_profile_registry = UserProfileRegistry()
