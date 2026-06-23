from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, Request
from app.infrastructure.grpc.clients.auth_client import AuthClient
from app.domain.exceptions import InvalidTokenException

security = HTTPBearer()

def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials
    
    try:
        client = AuthClient()
        user = client.validate(token)
        request.state.request_id = user.user_id
        return user
    except Exception:
        raise InvalidTokenException("Invalid or expired token")
