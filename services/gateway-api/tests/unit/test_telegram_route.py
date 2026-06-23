from app.api.dependencies.auth import get_current_user
from app.api.routes.auth import get_service

class FakeService:
    def update_telegram(self, user_id, token, chat_id, request_id: str | None = None):

        return type("obj", (), {"user_id": user_id})
    
def test_update_telegram(client):
    client.app.dependency_overrides[get_current_user] = lambda: type(
        "User", (), {"user_id": "1", "email": "test@test.com"}
    )
    client.app.dependency_overrides[get_service] = lambda: FakeService()
    response = client.put(
        "/auth/telegram",
        json={
            "telegram_token": "abc",
            "telegram_chat_id": "123"
        },
        headers={
            "Authorization": "Bearer valid-token"
        },
    )
    assert response.status_code == 200
    assert response.json()["user_id"] == "1"
    client.app.dependency_overrides.clear()

def test_update_telegram_invalid_token(client):
    response = client.put(
        "/auth/telegram",
        json={
            "telegram_token": "abc",
            "telegram_chat_id": "123"
        },
        headers={
            "Authorization": "Invalid header"
        },
    )
    assert response.status_code == 403
