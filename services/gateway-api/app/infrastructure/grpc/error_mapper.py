import grpc
from app.domain.exceptions import (
    AuthenticationException,
    AuthorizationException,
    ConflictException,
    ValidationException,
    NotFoundException,
    InvalidTokenException
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
    
    if status_code == grpc.StatusCode.INTERNAL:
        raise InvalidTokenException(details)
    
    raise Exception(f"gRPC error: {details}")
