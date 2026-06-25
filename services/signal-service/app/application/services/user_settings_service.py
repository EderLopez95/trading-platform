class UserSettingsService:
    def __init__(self, repository):
        self.repository = repository

    def get_status(self, user_id: str):
        return self._get_or_create(user_id)

    def toggle_analysis(self, user_id: str, enabled: bool):
        self._get_or_create(user_id)

        return self.repository.update_analysis_status(user_id, enabled)

    def _get_or_create(self, user_id: str):
        settings = self.repository.get_by_user(user_id)

        if settings:
            return settings

        return self.repository.create(user_id)
