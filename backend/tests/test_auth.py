import pytest
from fastapi import HTTPException
import hashlib


class TestAuthRoutes:
    """Test cases for authentication routes."""

    def test_register_success(self, client, db_session):
        """Test successful user registration."""
        user_data = {
            "name": "Test User",
            "email": "newuser@example.com",
            "password": "password123",
            "age": 25,
            "gender": "male",
        }

        response = client.post("/api/auth/register", json=user_data)
        assert response.status_code == 200
        assert response.json() == {"message": "User registered successfully"}

        # Verify user was created in database
        from models.user import User

        user = (
            db_session.query(User).filter(User.email == "newuser@example.com").first()
        )
        assert user is not None
        assert user.name == "Test User"
        assert user.age == 25

    def test_register_duplicate_email(self, client, test_user):
        """Test registration with duplicate email."""
        user_data = {
            "name": "Another User",
            "email": "test@example.com",  # Same as test_user
            "password": "password456",
            "age": 30,
            "gender": "female",
        }

        response = client.post("/api/auth/register", json=user_data)
        assert response.status_code == 400
        assert "User already exists" in response.json()["detail"]

    def test_register_invalid_data(self, client):
        """Test registration with invalid data."""
        user_data = {
            "name": "",  # Invalid: empty name
            "email": "invalid-email",  # Invalid email
            "password": "123",  # Too short
            "age": -5,  # Invalid age
            "gender": "other",
        }

        response = client.post("/api/auth/register", json=user_data)
        # Should fail validation
        assert response.status_code == 422  # Validation error

    def test_login_success(self, client, test_user):
        """Test successful login."""
        login_data = {"email": "test@example.com", "password": "password123"}

        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 200

        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert isinstance(data["access_token"], str)

    def test_login_invalid_email(self, client):
        """Test login with non-existent email."""
        login_data = {"email": "nonexistent@example.com", "password": "password123"}

        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]

    def test_login_wrong_password(self, client, test_user):
        """Test login with wrong password."""
        login_data = {"email": "test@example.com", "password": "wrongpassword"}

        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]

    def test_login_invalid_data(self, client):
        """Test login with invalid data."""
        login_data = {"email": "", "password": ""}  # Invalid email

        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 422  # Validation error


class TestAuthHelpers:
    """Test authentication helper functions."""

    def test_hash_password(self):
        """Test password hashing."""
        from routes.auth import hash_password

        password = "testpassword"
        hashed = hash_password(password)

        assert isinstance(hashed, str)
        assert len(hashed) == 64  # SHA256 hex length
        assert hashed == hashlib.sha256(password.encode()).hexdigest()

    def test_verify_password(self):
        """Test password verification."""
        from routes.auth import verify_password, hash_password

        password = "testpassword"
        hashed = hash_password(password)

        assert verify_password(password, hashed) is True
        assert verify_password("wrongpassword", hashed) is False

    def test_create_token(self):
        """Test JWT token creation."""
        from routes.auth import create_token
        import os

        # Set a test secret key
        os.environ["JWT_SECRET"] = "test_secret_key"

        data = {"sub": "test@example.com"}
        token = create_token(data)

        assert isinstance(token, str)
        assert len(token) > 0

        # Clean up
        del os.environ["JWT_SECRET"]
