from sqlalchemy.orm import Session
from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.database.models.user_model import UserModel
from app.domain.entities.user import User
import uuid

class UserRepositoryImpl(UserRepository):
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: str):
        return self.db.query(UserModel).filter(
            UserModel.id == user_id,
            UserModel.is_active == True
        ).first()

    def get_by_email(self, email: str):
        return self.db.query(UserModel).filter(
            UserModel.email == email,
            UserModel.is_active == True
        ).first()

    def create(self, email: str, password_hash: str):
        user = UserModel(
            id=uuid.uuid4(),
            email=email,
            password_hash=password_hash
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def _to_domain(self, model: UserModel) -> User:
        return User(
            id=model.id,
            email=model.email,
            password_hash=model.password_hash,
            telegram_token=model.telegram_token,
            telegram_chat_id=model.telegram_chat_id,
            is_active=model.is_active,
            created_at=model.created_at,
            deleted_at=model.deleted_at
        )
