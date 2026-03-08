import pytest
from datetime import datetime


class TestProgressRoutes:
    """Test cases for progress routes."""

    def test_get_overview_success(self, auth_client, db_session):
        """Test getting progress overview."""
        # Create some workout history
        from models.workout_history import WorkoutHistory

        for i in range(3):
            history = WorkoutHistory(
                user_id=1, workout_id=1, day=i + 1, calories=100 + i * 50
            )
            db_session.add(history)
        db_session.commit()

        response = auth_client.get("/api/progress/overview")
        assert response.status_code == 200

        data = response.json()
        assert data["workouts_completed"] == 3
        assert data["calories_burned"] == 450  # 100 + 150 + 200
        assert data["meals_tracked"] == 0

    def test_get_overview_no_data(self, auth_client):
        """Test getting progress overview with no data."""
        response = auth_client.get("/api/progress/overview")
        assert response.status_code == 200

        data = response.json()
        assert data["workouts_completed"] == 0
        assert data["calories_burned"] == 0
        assert data["meals_tracked"] == 0

    def test_workout_frequency_success(self, auth_client, db_session):
        """Test getting workout frequency."""
        from models.workout_history import WorkoutHistory

        # Create workouts on different days
        days = ["Mon", "Tue", "Mon", "Wed"]
        for i, day in enumerate(days):
            history = WorkoutHistory(user_id=1, workout_id=1, day=i + 1, calories=100)
            # Mock the completed_at date
            history.completed_at = datetime(2024, 1, i + 1)  # Different dates
            db_session.add(history)
        db_session.commit()

        response = auth_client.get("/api/progress/workouts")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 7  # 7 days of week

        # Check that all days are present
        day_names = [item["day"] for item in data]
        assert "Mon" in day_names
        assert "Tue" in day_names
        assert "Wed" in day_names

    def test_calories_chart_success(self, auth_client, db_session):
        """Test getting calories chart."""
        from models.workout_history import WorkoutHistory

        # Create 10 workouts to span multiple weeks
        for i in range(10):
            history = WorkoutHistory(user_id=1, workout_id=1, day=i + 1, calories=100)
            db_session.add(history)
        db_session.commit()

        response = auth_client.get("/api/progress/calories")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 4  # 4 weeks

        # Check week structure
        week_names = [item["week"] for item in data]
        assert "W1" in week_names
        assert "W2" in week_names

    def test_weight_history_success(self, auth_client, db_session):
        """Test getting weight history."""
        from models.body_metrics import BodyMetrics

        # Create weight entries
        weights = [70.5, 69.8, 69.2]
        for i, weight in enumerate(weights):
            metrics = BodyMetrics(
                user_id=1,
                height=170,
                weight=weight,
                bmi=24.0,
                body_fat_percent=15.0,
                muscle_mass=55.0,
            )
            db_session.add(metrics)
        db_session.commit()

        response = auth_client.get("/api/progress/weight-history")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3

        # Check weights are in order
        assert data[0]["weight"] == 70.5
        assert data[1]["weight"] == 69.8
        assert data[2]["weight"] == 69.2

    def test_weight_history_no_data(self, auth_client):
        """Test getting weight history with no data."""
        response = auth_client.get("/api/progress/weight-history")
        assert response.status_code == 200

        data = response.json()
        assert data == []

    def test_save_body_success(self, auth_client, db_session):
        """Test saving body metrics."""
        body_data = {"height": 175, "weight": 70}

        response = auth_client.post("/api/progress/body", json=body_data)
        assert response.status_code == 200
        assert response.json() == {"message": "Body metrics saved"}

        # Verify data was saved
        from models.body_metrics import BodyMetrics

        body = db_session.query(BodyMetrics).first()
        assert body is not None
        assert body.height == 175
        assert body.weight == 70
        assert round(body.bmi, 1) == 22.9  # 70 / (1.75^2)
        assert body.body_fat_percent == 16  # round(22.9 * 0.7)
        assert body.muscle_mass == 42  # round(70 * 0.6)

    def test_save_body_invalid_data(self, auth_client):
        """Test saving body metrics with invalid data."""
        body_data = {"height": 0, "weight": -10}  # Invalid  # Invalid

        response = auth_client.post("/api/progress/body", json=body_data)
        # Should still work as we don't validate input in the route
        assert response.status_code == 200

    def test_get_body_success(self, auth_client, db_session):
        """Test getting latest body metrics."""
        from models.body_metrics import BodyMetrics

        # Create body metrics
        metrics = BodyMetrics(
            user_id=1,
            height=170,
            weight=65,
            bmi=22.5,
            body_fat_percent=14.0,
            muscle_mass=39.0,
        )
        db_session.add(metrics)
        db_session.commit()

        response = auth_client.get("/api/progress/body")
        assert response.status_code == 200

        data = response.json()
        assert data["height"] == 170
        assert data["weight"] == 65
        assert data["bmi"] == 22.5
        assert data["body_fat_percent"] == 14.0
        assert data["muscle_mass"] == 39.0

    def test_get_body_no_data(self, auth_client):
        """Test getting body metrics when no data exists."""
        response = auth_client.get("/api/progress/body")
        assert response.status_code == 200

        data = response.json()
        assert data["height"] == 0
        assert data["weight"] == 0
        assert data["bmi"] == 0
        assert data["body_fat_percent"] == 0
        assert data["muscle_mass"] == 0

    def test_unauthorized_access(self, client):
        """Test that progress routes require authentication."""
        endpoints = [
            "/api/progress/overview",
            "/api/progress/workouts",
            "/api/progress/calories",
            "/api/progress/weight-history",
            "/api/progress/body",
        ]

        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code == 401
