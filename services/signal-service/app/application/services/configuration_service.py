import uuid
from app.domain.entities.configuration import Configuration

class ConfigurationService:
    def __init__(self, repository):
        self.repository = repository

    def get_configurations(self, user_id: str):
        return self.repository.get_by_user(user_id)

    def delete_configuration(self, configuration_id: str):
        self.repository.delete(configuration_id)

    def toggle_configuration(self, configuration_id: str, enabled: bool):
        configuration = self.repository.get_by_id(configuration_id)
        configuration.enabled = enabled
        return self.repository.update(configuration)

    def create_configuration(self, user_id: str, data: dict):
        configuration = Configuration(
            id=str(uuid.uuid4()),
            user_id=user_id,
            symbols=data["symbols"],
            strategies=data["strategies"],
            params=data.get("params"),
            trend_timeframe=data["trend_timeframe"],
            context_timeframe=data.get("context_timeframe"),
            entry_timeframe=data["entry_timeframe"],
            enabled=True,
            created_at=None,
        )
        return self.repository.create(configuration)
