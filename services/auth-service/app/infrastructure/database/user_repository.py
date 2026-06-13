from sqlalchemy.orm import Session
from shared.models.user_model import UserModel
import uuid

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

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
