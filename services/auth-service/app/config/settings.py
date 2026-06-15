import os
from dotenv import load_dotenv
from app.domain.exceptions import EnvironmentVariableMissingException

ENV = os.getenv("ENV", "local")

if ENV == "local":
    load_dotenv(".env.local")

ENV = os.getenv("ENV")
DATABASE_URL = os.getenv("DATABASE_URL")
JWT_SECRET = os.getenv("JWT_SECRET")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")
GRPC_PORT = int(os.getenv("GRPC_PORT", 5051))
GRPC_SSL_CERT = os.getenv("GRPC_SSL_CERT")
GRPC_SSL_KEY = os.getenv("GRPC_SSL_KEY")

def validate_settings():
    required = [
        "ENV",
        "DATABASE_URL",
        "JWT_SECRET",
        "ENCRYPTION_KEY",
        "GRPC_PORT"
    ]

    missing = [var for var in required if not os.getenv(var)]

    if missing:
        raise EnvironmentVariableMissingException(", ".join(missing))
