from app.infrastructure.scheduler.registry_container import user_registry

class UserSettingsService:
    def __init__(self, repository):
        self.repository = repository

    def get_status(self, user_id: str):
        return self._get_or_create(user_id)

    def toggle_analysis(self, user_id: str, enabled: bool):
        self._get_or_create(user_id)
        settings = self.repository.update_analysis_status(user_id, enabled)        
        user_registry.update(settings)

        return settings

    def _get_or_create(self, user_id: str):
        settings = self.repository.get_by_user(user_id)

        if settings:
            return settings

        return self.repository.create(user_id)
