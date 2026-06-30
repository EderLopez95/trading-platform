class DomainError(Exception):
    pass

class TimeframeNotSupportedException(DomainError):
    def __init__(self, timeframe: str = ""):
        super().__init__(f"Unsupported timeframe: {timeframe}")

class SymbolNotFoundException(DomainError):
    def __init__(self, symbol: str = ""):
        super().__init__(f"Symbol not found: {symbol}")

class RuntimeException(DomainError):
    def __init__(self, error: str = ""):
        super().__init__(error)

class EnvironmentVariableMissingException(DomainError):
    def __init__(self, var_name: str = ""):
        super().__init__(f"Missing environment variable: {var_name}")

class TLSMissingCertKeyException(DomainError):
    def __init__(self, var_name: str = ""):
        super().__init__(f"Missing TLS configuration: {var_name}")
