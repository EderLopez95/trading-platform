import pytest
from fastapi.testclient import TestClient
from main import app
from app.api.routes.auth import get_service

@pytest.fixture
def client(mock_auth_service):
    app.dependency_overrides[get_service] = lambda: mock_auth_service
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture
def mock_auth_service():
    class FakeUser:
        user_id = "1"
        email = "test@test.com"

    class FakeService:
        def register(self, email, password, request_id: str | None = None):

            return type("obj", (), {"user_id": "1", "token": "abc"})

        def login(self, email, password, request_id: str | None = None):

            return type("obj", (), {"user_id": "1", "token": "abc"})

        def validate(self, token, request_id: str | None = None):

            return FakeUser()

        def update_telegram(self, user_id, token, chat_id, request_id: str | None = None):

            return FakeUser()
        
    return FakeService()
