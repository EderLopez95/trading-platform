import uuid
from app.domain.entities.user import User

class FakeUserRepository:
    def __init__(self):
        self.users = {}

    def get_by_email(self, email: str):
        user = self.users.get(email)
        if user and user.is_active:
            return user
        return None

    def get_by_id(self, user_id: str):
        for user in self.users.values():
            if str(user.id) == str(user_id) and user.is_active:
                return user
        return None

    def create(self, email: str, password_hash: str):
        user = User(
            id=uuid.uuid4(),
            email=email,
            password_hash=password_hash,
            is_active=True
        )
        self.users[email] = user
        return user

    def update(self, user: User):
        self.users[user.email] = user
        return user

    def delete(self, user: User):
        user.is_active = False
        user.deleted_at = None
