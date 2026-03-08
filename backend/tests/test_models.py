import pytest
from models.user import User
from models.workout import WorkoutPlan
from models.nutrition import NutritionPlan
from models.progress import Progress
from models.health import HealthData
from models.workout_history import WorkoutHistory


class TestUserModel:
    """Test cases for User model."""

    def test_user_creation(self, db_session):
        """Test creating a new user."""
        user = User(
            name="John Doe",
            email="john@example.com",
            password="hashed_password",
            age=30,
            gender="male",
        )
        db_session.add(user)
        db_session.commit()

        assert user.id is not None
        assert user.name == "John Doe"
        assert user.email == "john@example.com"
        assert user.age == 30
        assert user.gender == "male"

    def test_user_unique_email(self, db_session):
        """Test that email must be unique."""
        user1 = User(
            name="User 1",
            email="duplicate@example.com",
            password="pass1",
            age=25,
            gender="female",
        )
        user2 = User(
            name="User 2",
            email="duplicate@example.com",
            password="pass2",
            age=26,
            gender="male",
        )

        db_session.add(user1)
        db_session.commit()

        db_session.add(user2)
        with pytest.raises(Exception):  # Should raise IntegrityError
            db_session.commit()


class TestWorkoutPlanModel:
    """Test cases for WorkoutPlan model."""

    def test_workout_plan_creation(self, db_session):
        """Test creating a workout plan."""
        plan = WorkoutPlan(
            user_id=1,
            goal="Weight Loss",
            level="Beginner",
            days=3,
            plan_json='{"test": "data"}',
            current_day=1,
        )
        db_session.add(plan)
        db_session.commit()

        assert plan.id is not None
        assert plan.user_id == 1
        assert plan.goal == "Weight Loss"
        assert plan.level == "Beginner"
        assert plan.days == 3
        assert plan.current_day == 1


class TestNutritionPlanModel:
    """Test cases for NutritionPlan model."""

    def test_nutrition_plan_creation(self, db_session):
        """Test creating a nutrition plan."""
        from models.nutrition import NutritionPlan

        plan = NutritionPlan(
            user_id=1, goal="Weight Loss", plan_json='{"meals": []}', current_day=1
        )
        db_session.add(plan)
        db_session.commit()

        assert plan.id is not None
        assert plan.user_id == 1
        assert plan.goal == "Weight Loss"


class TestProgressModel:
    """Test cases for Progress model."""

    def test_progress_creation(self, db_session):
        """Test creating a progress entry."""
        progress = Progress(
            user_id=1,
            date="2024-01-01",
            weight=70.5,
            body_fat=15.2,
            muscle_mass=60.3,
            notes="Good progress",
        )
        db_session.add(progress)
        db_session.commit()

        assert progress.id is not None
        assert progress.user_id == 1
        assert progress.weight == 70.5
        assert progress.body_fat == 15.2


class TestHealthDataModel:
    """Test cases for HealthData model."""

    def test_health_data_creation(self, db_session):
        """Test creating health data."""
        health = HealthData(
            user_id=1,
            date="2024-01-01",
            steps=10000,
            calories_burned=500,
            heart_rate=72,
            sleep_hours=8.0,
        )
        db_session.add(health)
        db_session.commit()

        assert health.id is not None
        assert health.user_id == 1
        assert health.steps == 10000
        assert health.calories_burned == 500


class TestWorkoutHistoryModel:
    """Test cases for WorkoutHistory model."""

    def test_workout_history_creation(self, db_session):
        """Test creating workout history."""
        history = WorkoutHistory(
            user_id=1,
            workout_plan_id=1,
            date="2024-01-01",
            day="Day 1",
            completed=True,
            duration_minutes=45,
            exercises_completed='["Push-ups", "Squats"]',
        )
        db_session.add(history)
        db_session.commit()

        assert history.id is not None
        assert history.user_id == 1
        assert history.completed is True
        assert history.duration_minutes == 45
