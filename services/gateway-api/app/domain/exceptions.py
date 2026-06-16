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
