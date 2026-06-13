class AuthException(Exception):
    pass

class UserAlreadyExistsException(AuthException):
    def __init__(self):
        super().__init__("User already exists")

class InvalidCredentialsException(AuthException):
    def __init__(self):
        super().__init__("Invalid credentials")

class TokenInvalidException(AuthException):
    def __init__(self):
        super().__init__("Invalid token")

class EnvironmentVariableMissingException(AuthException):
    def __init__(self, var_name: str):
        super().__init__(f"Missing environment variable: {var_name}")
