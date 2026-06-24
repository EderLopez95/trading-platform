import os
from dotenv import load_dotenv
from app.domain.exceptions import EnvironmentVariableMissingException

ENV = os.getenv("ENV", "local")

if ENV == "local":
    load_dotenv(".env.local")

ENV = os.getenv("ENV")
PORT = int(os.getenv("PORT", 8080))
AUTH_SERVICE_HOST = os.getenv("AUTH_SERVICE_HOST")
AUTH_SERVICE_PORT = int(os.getenv("AUTH_SERVICE_PORT", 5051))
AUTH_SERVICE_SECURE = (os.getenv("AUTH_SERVICE_SECURE", "false").strip().lower() == "true")
AUTH_SERVICE_CERT = os.getenv("AUTH_SERVICE_CERT")
SIGNAL_SERVICE_HOST = os.getenv("SIGNAL_SERVICE_HOST")
SIGNAL_SERVICE_PORT = int(os.getenv("SIGNAL_SERVICE_PORT", 5052))
JWT_SECRET = os.getenv("JWT_SECRET")

def validate_settings():
    required = [
        "ENV",
        "AUTH_SERVICE_HOST",
        "SIGNAL_SERVICE_HOST",
        "JWT_SECRET"
    ]

    missing = [var for var in required if not os.getenv(var)]

    if missing:
        raise EnvironmentVariableMissingException(", ".join(missing))

    if AUTH_SERVICE_SECURE and not AUTH_SERVICE_CERT:
        raise EnvironmentVariableMissingException("AUTH_SERVICE_CERT required when AUTH_SERVICE_SECURE=true")
