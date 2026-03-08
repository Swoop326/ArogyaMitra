import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from config.database import Base
from main import app
from routes.auth import get_db as auth_get_db

# Test database URL (use SQLite for testing)
TEST_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
test_engine = create_engine(
    TEST_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="function")
def db_session():
    """Create a test database session."""
    # Create all tables
    Base.metadata.create_all(bind=test_engine)

    # Create a session
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        # Drop all tables after test
        Base.metadata.drop_all(bind=test_engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with a test database."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[auth_get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(scope="function")
def test_user(db_session):
    """Create a test user."""
    from models.user import User
    import hashlib

    user = User(
        name="Test User",
        email="test@example.com",
        password=hashlib.sha256("password123".encode()).hexdigest(),
        age=25,
        gender="male",
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


# @pytest.fixture(scope="function")
# def auth_client(client, test_user):
#     """Create an authenticated test client."""
#     # Login to get token
#     login_data = {
#         "email": "test@example.com",
#         "password": "password123"
#     }
#     response = client.post("/api/auth/login", json=login_data)
#     token = response.json()["access_token"]

#     # Set authorization header for all requests
#     client.headers.update({"Authorization": f"Bearer {token}"})
#     return client</content>
# <parameter name="filePath">/Users/nandinigulhane/Documents/ArogyaMitra/backend/tests/conftest.py
