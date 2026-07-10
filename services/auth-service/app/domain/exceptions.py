class AuthException(Exception):
    pass

class UserAlreadyExistsException(AuthException):
    def __init__(self, message: str = "User already exists"):
        super().__init__(message)

class InvalidCredentialsException(AuthException):
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(message)

class EnvironmentVariableMissingException(AuthException):
    def __init__(self, var_name: str = ""):
        super().__init__(f"Missing environment variable: {var_name}")

class TLSMissingCertKeyException(AuthException):
    def __init__(self, var_name: str = ""):
        super().__init__(f"Missing TLS configuration: {var_name}")
