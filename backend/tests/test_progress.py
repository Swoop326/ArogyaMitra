def test_progress_overview(client):

    response = client.get("/api/progress/overview")

    assert response.status_code in [200, 401]


def test_progress_workouts(client):

    response = client.get("/api/progress/workouts")

    assert response.status_code in [200, 401]
