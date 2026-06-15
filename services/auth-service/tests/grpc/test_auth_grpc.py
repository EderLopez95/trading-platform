import grpc
import pytest
from app.infrastructure.protos.generated import auth_pb2, auth_pb2_grpc

@pytest.fixture(scope="module")
def grpc_channel(grpc_server):
    port, _ = grpc_server
    channel = grpc.insecure_channel(f"localhost:{port}")
    yield channel
    channel.close()

def test_register(grpc_channel):
    stub = auth_pb2_grpc.AuthServiceStub(grpc_channel)
    response = stub.Register(
        auth_pb2.RegisterRequest(
            email="grpc@test.com",
            password="123456"
        )
    )
    assert response.user_id != ""
    assert response.token != ""

def test_login(grpc_channel):
    stub = auth_pb2_grpc.AuthServiceStub(grpc_channel)
    stub.Register(
        auth_pb2.RegisterRequest(
            email="grpc2@test.com",
            password="123456"
        )
    )
    response = stub.Login(
        auth_pb2.LoginRequest(
            email="grpc2@test.com",
            password="123456"
        )
    )
    assert response.token != ""

def test_validate(grpc_channel):
    stub = auth_pb2_grpc.AuthServiceStub(grpc_channel)
    stub.Register(
        auth_pb2.RegisterRequest(
            email="grpc3@test.com",
            password="123456"
        )
    )
    login = stub.Login(
        auth_pb2.LoginRequest(
            email="grpc3@test.com",
            password="123456"
        )
    )
    response = stub.Validate(
        auth_pb2.ValidateRequest(token=login.token)
    )
    assert response.user_id != ""

def test_validate_invalid_token(grpc_channel):
    stub = auth_pb2_grpc.AuthServiceStub(grpc_channel)
    with pytest.raises(grpc.RpcError):
        stub.Validate(
            auth_pb2.ValidateRequest(token="invalid-token")
        )

def test_update_telegram(grpc_channel):
    stub = auth_pb2_grpc.AuthServiceStub(grpc_channel)
    register = stub.Register(
        auth_pb2.RegisterRequest(
            email="grpc4@test.com",
            password="123456"
        )
    )
    response = stub.UpdateTelegram(
        auth_pb2.UpdateTelegramRequest(
            user_id=register.user_id,
            telegram_token="token123",
            telegram_chat_id="chat123"
        )
    )
    assert response.user_id != ""
