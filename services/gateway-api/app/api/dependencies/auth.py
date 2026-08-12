from dataclasses import dataclass
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, Request
from app.config.settings import JWT_SECRET, JWT_ALGORITHM
from app.domain.exceptions import InvalidTokenException

security = HTTPBearer()

@dataclass
class AuthenticatedUser:
    user_id: str

def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> AuthenticatedUser:
    token = credentials.credentials

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError:
        raise InvalidTokenException("Invalid or expired token")

    user_id = payload.get("sub")

    if not user_id:
        raise InvalidTokenException("Invalid or expired token")

    request.state.user_id = user_id

    return AuthenticatedUser(user_id=user_id)

