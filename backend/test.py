import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import after loading env
from main import app
from config.database import Base, get_db
from models import user, workout, nutrition, progress, health, workout_history
import models.body_metrics
import models.health_profile

# Test database
TEST_DATABASE_URL = "sqlite:///./test_arogyamitra.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create test database tables
Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    # Drop tables after tests
    Base.metadata.drop_all(bind=engine)
    # Remove test database file
    if os.path.exists("./test_arogyamitra.db"):
        os.remove("./test_arogyamitra.db")


# Test data
test_user = {
    "name": "Test User",
    "email": "test@example.com",
    "password": "testpass123",
    "age": 25,
    "gender": "male",
}


class TestAuth:
    """Test authentication endpoints"""

    def test_register_success(self):
        response = client.post("/api/auth/register", json=test_user)
        assert response.status_code == 200
        assert response.json() == {"message": "User registered successfully"}

    def test_register_duplicate_email(self):
        # Try to register again with same email
        response = client.post("/api/auth/register", json=test_user)
        assert response.status_code == 400
        assert "User already exists" in response.json()["detail"]

    def test_login_success(self):
        response = client.post(
            "/api/auth/login",
            json={"email": test_user["email"], "password": test_user["password"]},
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"

        # Store token for other tests
        global auth_token
        auth_token = response.json()["access_token"]

    def test_login_invalid_credentials(self):
        response = client.post(
            "/api/auth/login",
            json={"email": "wrong@example.com", "password": "wrongpass"},
        )
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]

    def test_login_wrong_password(self):
        response = client.post(
            "/api/auth/login",
            json={"email": test_user["email"], "password": "wrongpass"},
        )
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]


class TestWorkouts:
    """Test workout endpoints"""

    def test_generate_workout_plan(self):
        headers = {"Authorization": f"Bearer {auth_token}"}
        workout_request = {"goal": "weight-loss", "level": "beginner", "days": 3}
        response = client.post(
            "/api/workouts/plan", json=workout_request, headers=headers
        )
        assert response.status_code == 200
        plan = response.json()
        assert "plan" in plan
        assert len(plan["plan"]) == 3

    def test_get_workout_day(self):
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.get("/api/workouts/day/1", headers=headers)
        assert response.status_code == 200
        day_plan = response.json()
        assert "day" in day_plan
        assert "exercises" in day_plan
        assert day_plan["day"] == "Day 1"

    def test_get_workout_day_not_found(self):
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.get(
            "/api/workouts/day/10", headers=headers
        )  # Day that doesn't exist
        assert response.status_code == 200
        assert response.json() == {"error": "Day not found"}

    def test_get_single_exercise(self):
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.get(
            "/api/workouts/exercise/1/0", headers=headers
        )  # Day 1, exercise 0
        assert response.status_code == 200
        exercise = response.json()
        assert "name" in exercise
        assert "sets" in exercise
        assert "reps" in exercise
        assert "exercise_index" in exercise

    def test_get_single_exercise_not_found(self):
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.get(
            "/api/workouts/exercise/1/100", headers=headers
        )  # Non-existent exercise
        assert response.status_code == 200
        assert response.json() == {"error": "Exercise not found"}

    def test_complete_workout_day(self):
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.post("/api/workouts/complete-day/1", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"message": "Day 1 completed successfully"}

    def test_complete_workout_day_already_completed(self):
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.post("/api/workouts/complete-day/1", headers=headers)
        assert response.status_code == 200
        assert response.json() == {"message": "Day 1 already completed"}

    def test_get_today_workout(self):
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.get("/api/workouts/today", headers=headers)
        assert response.status_code == 200
        today = response.json()
        assert "day" in today
        assert today["day"] == 2  # Since day 1 is completed


class TestNutrition:
    """Test nutrition endpoints"""

    def test_get_nutrition_plan(self):
        headers = {"Authorization": f"Bearer {auth_token}"}
        nutrition_request = {
            "goal": "weight-loss",
            "diet_type": "vegetarian",
            "calories": 2000,
        }
        response = client.post(
            "/api/nutrition/plan", json=nutrition_request, headers=headers
        )
        assert response.status_code == 200
        plan = response.json()
        assert "meals" in plan


class TestProgress:
    """Test progress tracking endpoints"""

    def test_get_progress(self):
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.get("/api/progress", headers=headers)
        assert response.status_code == 200
        # Should return empty or default progress initially


class TestHealth:
    """Test health endpoints"""

    def test_get_health_profile(self):
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.get("/api/health/profile", headers=headers)
        assert response.status_code == 200
        # May return empty if no profile exists


class TestDashboard:
    """Test dashboard endpoints"""

    def test_get_dashboard_stats(self):
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.get("/api/dashboard", headers=headers)
        assert response.status_code == 200
        stats = response.json()
        assert "workouts_completed" in stats
        assert "total_calories" in stats


class TestAI:
    """Test AI endpoints"""

    def test_ai_chat(self):
        headers = {"Authorization": f"Bearer {auth_token}"}
        chat_request = {"message": "Hello, how can you help me?"}
        response = client.post("/api/ai/chat", json=chat_request, headers=headers)
        assert response.status_code == 200
        response_data = response.json()
        assert "response" in response_data


class TestCalendar:
    """Test calendar endpoints"""

    def test_get_calendar_events(self):
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = client.get("/api/calendar", headers=headers)
        assert response.status_code == 200
        # Should return calendar events


class TestRoot:
    """Test root endpoint"""

    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "ArogyaMitra API Running 🚀"}


# Test unauthorized access
class TestUnauthorizedAccess:
    """Test that protected endpoints require authentication"""

    def test_workout_plan_unauthorized(self):
        workout_request = {"goal": "weight-loss", "level": "beginner", "days": 3}
        response = client.post("/api/workouts/plan", json=workout_request)
        assert response.status_code == 401

    def test_dashboard_unauthorized(self):
        response = client.get("/api/dashboard")
        assert response.status_code == 401


if __name__ == "__main__":
    pytest.main([__file__])
