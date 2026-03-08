import uuid


def test_register_user(client):

    email = f"user_{uuid.uuid4()}@example.com"

    payload = {
        "name": "Test User",
        "email": email,
        "password": "password123",
        "age": 25,
        "gender": "male"
    }

    response = client.post("/api/auth/register", json=payload)

    assert response.status_code in [200, 201]


def test_login_user(client):

    email = f"user_{uuid.uuid4()}@example.com"

    register_data = {
        "name": "Login User",
        "email": email,
        "password": "password123",
        "age": 25,
        "gender": "male"
    }

    client.post("/api/auth/register", json=register_data)

    response = client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": "password123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
