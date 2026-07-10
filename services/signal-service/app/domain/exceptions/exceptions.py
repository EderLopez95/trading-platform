class DomainError(Exception):
    pass

class ConfigurationNotFoundError(DomainError):
    def __init__(self, message: str = "Configuration not found"):
        super().__init__(message)

class EnvironmentVariableMissingException(DomainError):
    def __init__(self, var_name: str = ""):
        super().__init__(f"Missing environment variable: {var_name}")

class TLSMissingCertKeyException(DomainError):
    def __init__(self, var_name: str = ""):
        super().__init__(f"Missing TLS configuration: {var_name}")
