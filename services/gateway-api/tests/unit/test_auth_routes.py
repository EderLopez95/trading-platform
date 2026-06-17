from fastapi.testclient import TestClient
from app.api.routes.auth import get_service
from main import app
import pytest

class DummyService:
    def register(self, email, password, request_id):
        return type("obj", (), {"user_id": "1", "token": "abc"})

    def login(self, email, password, request_id):
        return type("obj", (), {"user_id": "1", "token": "abc"})

def override_get_service():
    return DummyService()

@app.middleware("http")
async def add_request_id_middleware(request, call_next):
    request.state.request_id = "test-request-id"
    return await call_next(request)

@pytest.fixture
def client():
    app.dependency_overrides[get_service] = lambda: DummyService()
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

def test_register(client):
    response = client.post(
        "/auth/register",
        json={"email": "test@test.com", "password": "123456"}
    )
    assert response.status_code == 200
    assert "token" in response.json()

def test_login(client):
    response = client.post(
        "/auth/login",
        json={"email": "test@test.com", "password": "123456"}
    )
    assert response.status_code == 200
    assert "token" in response.json()
