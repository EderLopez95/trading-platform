from app.api.auth_service import create_server
from app.config.settings import validate_settings
from app.core.logging.config import setup_logging

setup_logging()

def serve():
    validate_settings()
    server = create_server()
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
