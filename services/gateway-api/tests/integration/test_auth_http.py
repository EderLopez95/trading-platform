import requests

BASE_URL = "http://localhost:8080"

def test_full_flow():
    r = requests.post(
        f"{BASE_URL}/auth/register",
        json={"email": "int@test.com", "password": "123"}
    )
    assert r.status_code == 200
    r = requests.post(
        f"{BASE_URL}/auth/login",
        json={"email": "int@test.com", "password": "123"}
    )
    assert r.status_code == 200
    token = r.json()["token"]
    r = requests.put(
        f"{BASE_URL}/auth/telegram",
        json={
            "telegram_token": "abc",
            "telegram_chat_id": "123"
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert r.status_code == 200
