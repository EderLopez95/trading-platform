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

def validate_settings():
    required = [
        "ENV",
        "DATABASE_URL"
    ]

    missing = [var for var in required if not os.getenv(var)]

    if missing:
        raise EnvironmentVariableMissingException(", ".join(missing))
