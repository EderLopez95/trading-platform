import os
from dotenv import load_dotenv
from app.domain.exceptions.exceptions import EnvironmentVariableMissingException

ENV = os.getenv("ENV", "local")

if ENV == "local":
    load_dotenv(".env.local")

ENV = os.getenv("ENV")
DATABASE_URL = os.getenv("DATABASE_URL")
GRPC_PORT = int(os.getenv("GRPC_PORT", 5052))
GRPC_SSL_CERT = os.getenv("GRPC_SSL_CERT")
GRPC_SSL_KEY = os.getenv("GRPC_SSL_KEY")
MARKET_DATA_SERVICE_HOST = os.getenv("MARKET_DATA_SERVICE_HOST")
MARKET_DATA_SERVICE_PORT = int(os.getenv("MARKET_DATA_SERVICE_PORT", 5053))
SIGNAL_SERVICE_SECURE = (os.getenv("SIGNAL_SERVICE_SECURE", "false").strip().lower() == "true")
SIGNAL_SERVICE_CERT = os.getenv("SIGNAL_SERVICE_CERT")

def validate_settings():
    required = [
        "ENV",
        "DATABASE_URL",
        "MARKET_DATA_SERVICE_HOST",
    ]

    missing = [var for var in required if not os.getenv(var)]

    if missing:
        raise EnvironmentVariableMissingException(", ".join(missing))

    if SIGNAL_SERVICE_SECURE and not SIGNAL_SERVICE_CERT:
        raise EnvironmentVariableMissingException("SIGNAL_SERVICE_SECURE required when SIGNAL_SERVICE_CERT=true")
