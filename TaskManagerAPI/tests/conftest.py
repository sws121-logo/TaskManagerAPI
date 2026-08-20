import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.database import Base, get_db
from src.security import get_password_hash
from src.models import User

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session")
def db_engine():
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def db_session(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def test_user(db_session):
    user = User(
        email="test@example.com",
        hashed_password=get_password_hash("TestPass123"),
        full_name="Test User"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

@pytest.fixture
def auth_token(client, test_user):
    response = client.post(
        "/api/auth/login",
        data={"username": "test@example.com", "password": "TestPass123"}
    )
    return response.json()["access_token"]

@pytest.fixture
def authenticated_client(client, auth_token):
    client.headers.update({"Authorization": f"Bearer {auth_token}"})
    return client
