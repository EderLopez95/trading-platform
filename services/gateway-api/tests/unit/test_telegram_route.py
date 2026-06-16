from app.api.dependencies.auth import get_current_user

def test_update_telegram(client):
    client.app.dependency_overrides[get_current_user] = lambda: type(
        "User", (), {"user_id": "1", "email": "test@test.com"}
    )
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
    assert response.status_code == 401
