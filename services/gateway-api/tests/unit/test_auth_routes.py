from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register(client):
    response = client.post(
        "/auth/register",
        json={"email": "test@test.com", "password": "123"}
    )
    assert response.status_code == 200
    assert "token" in response.json()

def test_login(client):
    response = client.post(
        "/auth/login",
        json={"email": "test@test.com", "password": "123"}
    )
    assert response.status_code == 200
    assert "token" in response.json()
