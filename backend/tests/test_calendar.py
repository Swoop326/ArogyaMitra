def test_calendar_route(client):

    response = client.get("/api/calendar/")

    assert response.status_code == 200
    assert response.json()["message"] == "Calendar integration working"
