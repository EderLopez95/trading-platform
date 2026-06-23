class DomainError(Exception):
    pass

class InvalidConfigError(DomainError):
    def __init__(self, message: str = "Invalid configuration"):
        super().__init__(message)

class StrategyNotFoundError(DomainError):
    def __init__(self, message: str = "Strategy not found"):
        super().__init__(message)

class ConfigurationNotFoundError(DomainError):
    def __init__(self, message: str = "Configuration not found"):
        super().__init__(message)

class BotAlreadyRunningError(DomainError):
    def __init__(self, message: str = "Bot already running"):
        super().__init__(message)

class BotNotRunningError(DomainError):
    def __init__(self, message: str = "Bot not running"):
        super().__init__(message)

class EnvironmentVariableMissingException(DomainError):
    def __init__(self, var_name: str = ""):
        super().__init__(f"Missing environment variable: {var_name}")

class TLSMissingCertKeyException(DomainError):
    def __init__(self, var_name: str = ""):
        super().__init__(f"Missing TLS configuration: {var_name}")
