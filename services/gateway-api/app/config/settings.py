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
GATEWAY_SERVICE_SECURE = (os.getenv("GATEWAY_SERVICE_SECURE", "false").strip().lower() == "true")
TRUSTED_CA_CERT = os.getenv("TRUSTED_CA_CERT")
SIGNAL_SERVICE_HOST = os.getenv("SIGNAL_SERVICE_HOST")
SIGNAL_SERVICE_PORT = int(os.getenv("SIGNAL_SERVICE_PORT", 5052))
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "http://localhost:3002").split(",") if o.strip()]
CORS_ALLOW_METHODS = [m.strip() for m in os.getenv("CORS_ALLOW_METHODS", "*").split(",") if m.strip()]
CORS_ALLOW_HEADERS = [h.strip() for h in os.getenv("CORS_ALLOW_HEADERS", "*").split(",") if h.strip()]
LOGIN_RATE_LIMIT_MAX = int(os.getenv("LOGIN_RATE_LIMIT_MAX", 5))
LOGIN_RATE_LIMIT_WINDOW = int(os.getenv("LOGIN_RATE_LIMIT_WINDOW", 60))

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

    if GATEWAY_SERVICE_SECURE and not TRUSTED_CA_CERT:
        raise EnvironmentVariableMissingException("TRUSTED_CA_CERT required when GATEWAY_SERVICE_SECURE=true")
