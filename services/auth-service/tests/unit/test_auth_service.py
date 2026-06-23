import pytest
from app.application.services.auth_service import AuthService
from app.domain.exceptions import UserAlreadyExistsException, InvalidCredentialsException
from tests.fakes.fake_user_repository import FakeUserRepository

def test_register_success():
    repo = FakeUserRepository()
    service = AuthService(repo)
    result = service.register("test@test.com", "123456")
    assert result["token"] == "fake-token"

def test_register_duplicate():
    repo = FakeUserRepository()
    service = AuthService(repo)
    service.register("test@test.com", "123")
    with pytest.raises(UserAlreadyExistsException):
        service.register("test@test.com", "123")

def test_login_success():
    repo = FakeUserRepository()
    service = AuthService(repo)
    service.register("test@test.com", "123")
    result = service.login("test@test.com", "123")
    assert result["token"] == "fake-token"

def test_login_invalid_email():
    repo = FakeUserRepository()
    service = AuthService(repo)
    with pytest.raises(InvalidCredentialsException):
        service.login("fake@test.com", "123")

def test_login_invalid_password(monkeypatch):
    repo = FakeUserRepository()
    service = AuthService(repo)
    service.register("test@test.com", "123")
    monkeypatch.setattr(
        "app.application.services.auth_service.verify_password",
        lambda a, b: False
    )
    with pytest.raises(InvalidCredentialsException):
        service.login("test@test.com", "123")

def test_login_after_delete():
    repo = FakeUserRepository()
    service = AuthService(repo)
    service.register("test@test.com", "123")
    user = repo.get_by_email("test@test.com")
    repo.delete(user)
    with pytest.raises(InvalidCredentialsException):
        service.login("test@test.com", "123")
