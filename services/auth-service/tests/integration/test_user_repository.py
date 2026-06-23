from app.infrastructure.database.user_repository_impl import UserRepositoryImpl

def test_create_user(db_session):
    repo = UserRepositoryImpl(db_session)
    user = repo.create("repo@test.com", "hash")
    assert user.id is not None
    assert user.email == "repo@test.com"

def test_get_user_by_id(db_session):
    repo = UserRepositoryImpl(db_session)
    user = repo.create("repo@test.com", "hash")
    found = repo.get_by_id(user.id)
    assert found is not None
    assert found.id == user.id

def test_update_user(db_session):
    repo = UserRepositoryImpl(db_session)
    user = repo.create("repo@test.com", "hash")
    user.email = "updated@test.com"
    repo.update(user)
    updated = repo.get_by_id(user.id)
    assert updated.email == "updated@test.com"

def test_delete_user(db_session):
    repo = UserRepositoryImpl(db_session)
    user = repo.create("repo@test.com", "hash")
    repo.delete(user)
    deleted = repo.get_by_id(user.id)
    assert deleted is None

def test_update_telegram(db_session):
    repo = UserRepositoryImpl(db_session)
    user = repo.create("repo@test.com", "hash")
    updated = repo.update_telegram(user, "token123", "chat123")
    assert updated.telegram_token != "token123"
    assert updated.telegram_chat_id != "chat123"
