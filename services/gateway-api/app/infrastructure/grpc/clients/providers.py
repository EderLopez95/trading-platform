from functools import lru_cache
from app.infrastructure.grpc.clients.auth_client import AuthClient
from app.infrastructure.grpc.clients.signal_client import SignalClient

@lru_cache(maxsize=1)
def get_auth_client() -> AuthClient:

    return AuthClient()

@lru_cache(maxsize=1)
def get_signal_client() -> SignalClient:

    return SignalClient()
