from app.domain.repositories.user_repository import UserRepository
from app.infrastructure.security.password_hasher import hash_password, verify_password
from app.infrastructure.security.jwt_handler import create_token
from app.domain.exceptions import UserAlreadyExistsException, InvalidCredentialsException
from app.domain.entities.user import UserResponse

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register(self, email: str, password: str):
        existing = self.user_repo.get_by_email(email)
        
        if existing:
            raise UserAlreadyExistsException()

        password_hash = hash_password(password)
        user = self.user_repo.create(email, password_hash)
        token = create_token(str(user.id))

        return UserResponse(
            user_id=str(user.id),
            token=token
        )

    def login(self, email: str, password: str):
        user = self.user_repo.get_by_email(email)

        if not user:
            raise InvalidCredentialsException()

        if not verify_password(password, user.password_hash):
            raise InvalidCredentialsException()

        token = create_token(str(user.id))
        
        return UserResponse(
            user_id=str(user.id),
            token=token
        )

    def validate_user(self, user_id: str):
        user = self.user_repo.get_by_id(user_id)

        if not user:
            raise InvalidCredentialsException()

        return user

    def update_telegram(self, user_id: str, token: str, chat_id: str):
        user = self.user_repo.get_by_id(user_id)

        if not user:
            raise InvalidCredentialsException()

        return self.user_repo.update_telegram(user, token, chat_id)
