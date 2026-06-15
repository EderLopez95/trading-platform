from app.api.grpc_server import create_server
from app.config.settings import validate_settings

def serve():
    validate_settings()
    server = create_server()
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()
