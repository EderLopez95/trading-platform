import grpc
from concurrent import futures
from app.config.settings import ENV, GRPC_PORT, GRPC_SSL_CERT, GRPC_SSL_KEY
from app.domain.exceptions.exceptions import TLSMissingCertKeyException
from app.infrastructure.protos.generated import signals_pb2_grpc
from app.api.signals_service import SignalsGrpcService

def create_server():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )
    signals_pb2_grpc.add_SignalsServiceServicer_to_server(
        SignalsGrpcService(),
        server
    )
    address = f"[::]:{GRPC_PORT}"
    
    if ENV == "prod":
        _add_secure_port(server, address)
        print(f"gRPC Secure server running on {address}")
    else:
        server.add_insecure_port(address)
        print(f"gRPC Insecure server running on {address}")

    return server

def _add_secure_port(server, address):
    if not GRPC_SSL_CERT or not GRPC_SSL_KEY:
        raise TLSMissingCertKeyException("GRPC_SSL_CERT / GRPC_SSL_KEY")

    with open(GRPC_SSL_CERT, "rb") as f:
        certificate_chain = f.read()
    with open(GRPC_SSL_KEY, "rb") as f:
        private_key = f.read()

    server_credentials = grpc.ssl_server_credentials(
        [(private_key, certificate_chain)]
    )
    server.add_secure_port(address, server_credentials)
