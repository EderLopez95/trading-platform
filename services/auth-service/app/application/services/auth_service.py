from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.security.password_hasher import hash_password, verify_password
from app.infrastructure.security.jwt_handler import create_token
from app.domain.exceptions import UserAlreadyExistsException, InvalidCredentialsException

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register(self, email, password):
        if self.user_repo.get_by_email(email):
            raise UserAlreadyExistsException()

        hashed = hash_password(password)
        user = self.user_repo.create(email, hashed)
        token = create_token(str(user.id))
        return {
            "user_id": str(user.id),
            "token": token
        }

    def login(self, email, password):
        user = self.user_repo.get_by_email(email)

        if not user:
            raise InvalidCredentialsException()

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsException()

        token = create_token(str(user.id))
        return {
            "user_id": str(user.id),
            "token": token
        }
