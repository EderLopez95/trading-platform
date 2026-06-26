from app.api.grpc_server import create_server
from app.config.settings import validate_settings
from app.core.logging.config import setup_logging
from app.core.registry.registry import load_registries

setup_logging()

def serve():
    validate_settings()
    load_registries()
    server = create_server()
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
