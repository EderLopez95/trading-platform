class GatewayAPIException(Exception):
    pass

class AuthenticationException(GatewayAPIException):
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message)

class AuthorizationException(GatewayAPIException):
    def __init__(self, message: str = "Unauthorized access"):
        super().__init__(message)

class InvalidTokenException(GatewayAPIException):
    def __init__(self, message: str = "Invalid token"):
        super().__init__(message)

class EnvironmentVariableMissingException(GatewayAPIException):
    def __init__(self, variables: str = ""):
        super().__init__(f"Missing environment variables: {variables}")

class NotFoundException(GatewayAPIException):
    def __init__(self, message="Resource not found"):
        super().__init__(message)

class ValidationException(GatewayAPIException):
    def __init__(self, message="Invalid input"):
        super().__init__(message)

class ConflictException(GatewayAPIException):
    def __init__(self, message="Conflict"):
        super().__init__(message)

class ServiceUnavailableException(GatewayAPIException):
    def __init__(self, message="Service temporarily unavailable"):
        super().__init__(message)

class RateLimitExceededException(GatewayAPIException):
    def __init__(self, message="Too many requests"):
        super().__init__(message)
