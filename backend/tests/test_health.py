def test_health_debug(client):

    response = client.get("/api/health/debug")

    assert response.status_code == 200

    data = response.json()

    assert "count" in data
    assert "profiles" in data
