import os

os.environ["DATABASE_URL"] = "postgresql://trading:trading@postgres:5432/trading_platform_test"

import pytest
from unittest.mock import patch
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.infrastructure.database.models.base import Base
from app.api.auth_service import create_server

engine = create_engine(os.environ["DATABASE_URL"])
SessionTesting = sessionmaker(bind=engine)

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    with engine.connect() as conn:
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS auth"))
        conn.commit()
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    with engine.connect() as conn:
        conn.execute(text("DROP SCHEMA IF EXISTS auth CASCADE"))
        conn.commit()

@pytest.fixture(scope="function")
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionTesting(bind=connection)
    yield session
    transaction.rollback()
    session.close()
    connection.close()

@pytest.fixture(autouse=True)
def clean_db():
    with engine.connect() as conn:
        conn.execute(text("TRUNCATE TABLE auth.users RESTART IDENTITY CASCADE"))
        conn.commit()
    yield

@pytest.fixture(autouse=True)
def mock_security(request):
    if "unit" not in str(request.node.fspath):
        yield
        return
    
    with patch("app.application.services.auth_service.hash_password") as mock_hash, \
         patch("app.application.services.auth_service.verify_password") as mock_verify, \
         patch("app.application.services.auth_service.create_token") as mock_jwt:

        mock_hash.return_value = "hashed"
        mock_verify.return_value = True
        mock_jwt.return_value = "fake-token"
        yield

@pytest.fixture(scope="session")
def grpc_server():
    server = create_server()
    port = server.add_insecure_port("localhost:0")
    server.start()
    yield port, server
    server.stop(0)
