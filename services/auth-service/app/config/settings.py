import os
from dotenv import load_dotenv
from app.domain.exceptions import EnvironmentVariableMissingException

ENV = os.getenv("ENV", "local")

if ENV == "local":
    load_dotenv(".env.local")

DATABASE_URL = os.getenv("DATABASE_URL")
JWT_SECRET = os.getenv("JWT_SECRET")
ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY")

def validate_settings():
    required = [
        "DATABASE_URL",
        "JWT_SECRET",
        "ENCRYPTION_KEY"
    ]

    missing = [var for var in required if not os.getenv(var)]

    if missing:
        raise EnvironmentVariableMissingException(", ".join(missing))
