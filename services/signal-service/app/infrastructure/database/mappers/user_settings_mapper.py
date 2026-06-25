from app.domain.entities.user_settings import UserSettings

class UserSettingsMapper:
    @staticmethod
    def to_domain(model):

        return UserSettings(
            id=str(model.id),
            user_id=str(model.user_id),
            analysis_enabled=model.analysis_enabled
        )
