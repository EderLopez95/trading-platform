from fastapi import Header
from app.infrastructure.grpc.clients.auth_client import AuthClient
from app.domain.exceptions import InvalidTokenException

def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise InvalidTokenException("Invalid authorization header")

    token = authorization.replace("Bearer ", "")

    try:
        client = AuthClient()
        user = client.validate(token)
        return user
    except Exception:
        raise InvalidTokenException("Invalid or expired token")
