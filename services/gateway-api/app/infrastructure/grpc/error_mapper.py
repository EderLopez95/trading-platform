import grpc
from app.domain.exceptions import (
    AuthenticationException,
    AuthorizationException,
    ConflictException,
    ValidationException,
    NotFoundException,
    ServiceUnavailableException
)

def map_grpc_error(error: grpc.RpcError):
    status_code = error.code()
    details = error.details()

    if status_code == grpc.StatusCode.UNAUTHENTICATED:
        raise AuthenticationException(details)

    if status_code == grpc.StatusCode.PERMISSION_DENIED:
        raise AuthorizationException(details)
    
    if status_code == grpc.StatusCode.INVALID_ARGUMENT:
        raise ValidationException(details)

    if status_code == grpc.StatusCode.NOT_FOUND:
        raise NotFoundException(details)
        
    if status_code == grpc.StatusCode.ALREADY_EXISTS:
        raise ConflictException(details)

    if status_code in (grpc.StatusCode.UNAVAILABLE, grpc.StatusCode.DEADLINE_EXCEEDED):
        raise ServiceUnavailableException(details or "Service temporarily unavailable")
    
    raise Exception(f"gRPC error: {details}")
