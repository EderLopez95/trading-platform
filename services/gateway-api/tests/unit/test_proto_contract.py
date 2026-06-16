from app.infrastructure.protos.generated import auth_pb2

def test_register_request_contract():
    req = auth_pb2.RegisterRequest(
        email="test@test.com",
        password="123456"
    )
    assert req.email == "test@test.com"
    assert req.password == "123456"

def test_login_request_contract():
    req = auth_pb2.LoginRequest(
        email="a@a.com",
        password="123"
    )
    assert isinstance(req.email, str)
    assert isinstance(req.password, str)

def test_update_telegram_request_contract():
    req = auth_pb2.UpdateTelegramRequest(
        user_id="1",
        telegram_token="token",
        telegram_chat_id="chat"
    )
    assert req.telegram_token == "token"

def test_auth_response_contract():
    res = auth_pb2.AuthResponse(
        user_id="1",
        token="abc"
    )
    assert res.token == "abc"

def test_user_response_contract():
    res = auth_pb2.UserResponse(
        user_id="1",
        email="test@test.com"
    )
    assert res.email == "test@test.com"
