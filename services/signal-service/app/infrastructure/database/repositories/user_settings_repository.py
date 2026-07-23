import uuid
from sqlalchemy.orm import Session
from app.infrastructure.database.models.user_settings import UserSettingsModel
from app.infrastructure.database.mappers.user_settings_mapper import UserSettingsMapper

class UserSettingsRepositoryImpl:
    def __init__(self, db: Session):
        self.db = db

    def get_by_user(self, user_id: str):
        model = (
            self.db.query(UserSettingsModel)
            .filter(UserSettingsModel.user_id == uuid.UUID(user_id))
            .first()
        )

        if not model:
            return None

        return UserSettingsMapper.to_domain(model)

    def create(self, user_id: str):
        model = UserSettingsModel(
            user_id=uuid.UUID(user_id),
            analysis_enabled=False,
        )
        self.db.add(model)
        self.db.commit()
        self.db.refresh(model)

        return UserSettingsMapper.to_domain(model)

    def update_analysis_status(self, user_id: str, enabled: bool):
        model = (
            self.db.query(UserSettingsModel)
            .filter(UserSettingsModel.user_id == uuid.UUID(user_id))
            .first()
        )
        model.analysis_enabled = enabled
        self.db.commit()
        self.db.refresh(model)

        return UserSettingsMapper.to_domain(model)

    def get_users(self):
        models = (
            self.db.query(UserSettingsModel)
            .all()
        )

        return [
            UserSettingsMapper.to_domain(model)
            for model in models
        ]
