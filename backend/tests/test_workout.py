def test_get_today_workout(client):

    response = client.get("/api/workouts/today")

    assert response.status_code in [200, 401]


def test_get_workout_day(client):

    response = client.get("/api/workouts/day/1")

    assert response.status_code in [200, 401]
