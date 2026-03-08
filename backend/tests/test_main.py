import pytest


class TestMainApp:
    """Test cases for main FastAPI app."""

    def test_root_endpoint(self, client):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "ArogyaMitra API Running 🚀"}

    def test_openapi_docs_available(self, client):
        """Test that OpenAPI docs are available."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_openapi_json_available(self, client):
        """Test that OpenAPI JSON is available."""
        response = client.get("/openapi.json")
        assert response.status_code == 200

        data = response.json()
        assert "info" in data
        assert "paths" in data


class TestHealthRoutes:
    """Test cases for health routes."""

    def test_health_data_creation(self, auth_client, db_session):
        """Test creating health data."""
        from models.health import HealthData

        health_data = {
            "date": "2024-01-01",
            "steps": 10000,
            "calories_burned": 500,
            "heart_rate": 72,
            "sleep_hours": 8.0,
        }

        response = auth_client.post("/api/health/data", json=health_data)
        assert response.status_code == 200

        # Verify data was saved
        health = db_session.query(HealthData).first()
        assert health is not None
        assert health.steps == 10000
        assert health.calories_burned == 500

    def test_get_health_data(self, auth_client, db_session):
        """Test getting health data."""
        from models.health import HealthData

        # Create health data
        health = HealthData(
            user_id=1,
            date="2024-01-01",
            steps=8000,
            calories_burned=400,
            heart_rate=70,
            sleep_hours=7.5,
        )
        db_session.add(health)
        db_session.commit()

        response = auth_client.get("/api/health/data")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 1
        assert data[0]["steps"] == 8000


class TestDashboardRoutes:
    """Test cases for dashboard routes."""

    def test_get_dashboard_stats(self, auth_client, db_session):
        """Test getting dashboard statistics."""
        # Create some test data
        from models.workout_history import WorkoutHistory
        from models.body_metrics import BodyMetrics

        # Add workout history
        history = WorkoutHistory(user_id=1, workout_id=1, day=1, calories=200)
        db_session.add(history)

        # Add body metrics
        metrics = BodyMetrics(
            user_id=1,
            height=170,
            weight=70,
            bmi=24.2,
            body_fat_percent=16.9,
            muscle_mass=42.0,
        )
        db_session.add(metrics)
        db_session.commit()

        response = auth_client.get("/api/dashboard/stats")
        assert response.status_code == 200

        data = response.json()
        assert "total_workouts" in data
        assert "total_calories" in data
        assert "current_weight" in data
        assert "current_bmi" in data


class TestAIRoutes:
    """Test cases for AI routes."""

    def test_ai_coach_response(self, auth_client):
        """Test AI coach endpoint."""
        message_data = {"message": "How to stay motivated?"}

        response = auth_client.post("/api/ai/coach", json=message_data)
        assert response.status_code == 200

        data = response.json()
        assert "reply" in data
        assert "AROMI AI Coach says:" in data["reply"]


class TestCalendarRoutes:
    """Test cases for calendar routes."""

    def test_get_calendar_data(self, auth_client, db_session):
        """Test getting calendar workout data."""
        from models.workout_history import WorkoutHistory

        # Create workout history with dates
        for i in range(3):
            history = WorkoutHistory(user_id=1, workout_id=1, day=i + 1, calories=100)
            db_session.add(history)
        db_session.commit()

        response = auth_client.get("/api/calendar/workouts")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)
