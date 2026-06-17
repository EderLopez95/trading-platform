from app.application.services.auth_service import AuthService

class DummyClient:
    def register(self, email, password, request_id):
        return type("obj", (), {"user_id": "1", "token": "abc"})

    def login(self, email, password, request_id):
        return type("obj", (), {"user_id": "1", "token": "abc"})

    def validate(self, token, request_id):
        return type("obj", (), {"user_id": "1", "email": "test@test.com"})

    def update_telegram(self, user_id, token, chat_id, request_id):
        return type("obj", (), {"user_id": user_id})

def test_register():
    service = AuthService(DummyClient())
    res = service.register("test@test.com", "123")
    assert res.token == "abc"

def test_login():
    service = AuthService(DummyClient())
    res = service.login("test@test.com", "123")
    assert res.token == "abc"

def test_validate():
    service = AuthService(DummyClient())
    res = service.validate("token")
    assert res.user_id == "1"
