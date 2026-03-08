def test_dashboard_route(client):

    response = client.get("/api/dashboard")

    assert response.status_code in [200, 401]
