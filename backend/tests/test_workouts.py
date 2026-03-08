import pytest
from unittest.mock import patch, MagicMock
import json


class TestWorkoutRoutes:
    """Test cases for workout routes."""

    @patch("services.workout_service.generate_workout_plan")
    def test_generate_plan_success(self, mock_generate, auth_client, db_session):
        """Test successful workout plan generation."""

        mock_plan = {
            "plan": [
                {
                    "day": "Day 1",
                    "workout": "Upper Body",
                    "exercises": [{"name": "Push-ups", "sets": 3, "reps": 10}],
                }
            ]
        }
        mock_generate.return_value = mock_plan

        plan_data = {"goal": "weight-loss", "level": "beginner", "days": 3}

        response = auth_client.post("/api/workouts/plan", json=plan_data)
        assert response.status_code == 200

        data = response.json()
        assert "plan" in data
        assert len(data["plan"]) == 1
        assert data["plan"][0]["day"] == "Day 1"

        from models.workout import WorkoutPlan

        plan = db_session.query(WorkoutPlan).first()
        assert plan is not None
        assert plan.goal == "weight_loss"
        assert plan.level == "beginner"
        assert plan.days == 3

    def test_generate_plan_unauthorized(self, client):
        """Test workout plan generation without authentication."""
        plan_data = {"goal": "weight-loss", "level": "beginner", "days": 3}

        response = client.post("/api/workouts/plan", json=plan_data)
        assert response.status_code == 401

    @patch("services.workout_service.generate_workout_plan")
    def test_get_workout_day_success(self, mock_generate, auth_client, db_session):
        """Test getting a specific workout day."""

        mock_plan = {
            "plan": [
                {
                    "day": "Day 1",
                    "workout": "Upper Body",
                    "exercises": [{"name": "Push-ups", "sets": 3, "reps": 10}],
                },
                {
                    "day": "Day 2",
                    "workout": "Lower Body",
                    "exercises": [{"name": "Squats", "sets": 3, "reps": 12}],
                },
            ]
        }
        mock_generate.return_value = mock_plan

        plan_data = {"goal": "weight-loss", "level": "beginner", "days": 3}
        auth_client.post("/api/workouts/plan", json=plan_data)

        response = auth_client.get("/api/workouts/day/1")
        assert response.status_code == 200

        data = response.json()
        assert data["day"] == "Day 1"
        assert data["workout"] == "Upper Body"
        assert len(data["exercises"]) == 1

    def test_get_workout_day_no_plan(self, auth_client):
        """Test getting workout day when no plan exists."""
        response = auth_client.get("/api/workouts/day/1")
        assert response.status_code == 200
        assert response.json() == {"error": "No workout plan found"}

    def test_get_workout_day_invalid_day(self, auth_client, db_session):
        """Test getting invalid workout day."""

        from models.workout import WorkoutPlan

        plan = WorkoutPlan(
            user_id=1,
            goal="weight_loss",
            level="beginner",
            days=2,
            plan_json=json.dumps(
                {
                    "plan": [
                        {"day": "Day 1", "workout": "Upper", "exercises": []},
                        {"day": "Day 2", "workout": "Lower", "exercises": []},
                    ]
                }
            ),
        )
        db_session.add(plan)
        db_session.commit()

        response = auth_client.get("/api/workouts/day/5")
        assert response.status_code == 200
        assert response.json() == {"error": "Day not found"}

    @patch("routes.workouts.get_youtube_video")
    def test_get_single_exercise_success(self, mock_youtube, auth_client, db_session):
        """Test getting a single exercise."""
        mock_youtube.return_value = "https://youtube.com/embed/test"

        from models.workout import WorkoutPlan

        plan = WorkoutPlan(
            user_id=1,
            goal="weight_loss",
            level="beginner",
            days=3,
            plan_json=json.dumps(
                {
                    "plan": [
                        {
                            "day": "Day 1",
                            "workout": "Upper Body",
                            "exercises": [
                                {"name": "Push-ups", "sets": 3, "reps": 10},
                                {"name": "Pull-ups", "sets": 3, "reps": 8},
                            ],
                        }
                    ]
                }
            ),
        )
        db_session.add(plan)
        db_session.commit()

        response = auth_client.get("/api/workouts/exercise/1/0")
        assert response.status_code == 200

        data = response.json()
        assert data["name"] == "Push-ups"
        assert data["sets"] == 3
        assert data["reps"] == 10
        assert "video" in data
        assert "calories" in data

    def test_get_single_exercise_no_plan(self, auth_client):
        """Test getting exercise when no plan exists."""
        response = auth_client.get("/api/workouts/exercise/1/0")
        assert response.status_code == 200
        assert response.json() == {"error": "No workout plan"}

    def test_complete_day_success(self, auth_client, db_session):
        """Test completing a workout day."""

        from models.workout import WorkoutPlan

        plan = WorkoutPlan(
            user_id=1,
            goal="weight_loss",
            level="beginner",
            days=3,
            plan_json=json.dumps({"plan": []}),
        )
        db_session.add(plan)
        db_session.commit()

        response = auth_client.post("/api/workouts/complete-day/1")
        assert response.status_code == 200
        assert response.json() == {"message": "Day 1 completed successfully"}

        from models.workout_history import WorkoutHistory

        history = db_session.query(WorkoutHistory).first()
        assert history is not None
        assert history.day == 1
        assert history.calories == 100

    def test_complete_day_already_completed(self, auth_client, db_session):
        """Test completing a day that's already completed."""

        from models.workout import WorkoutPlan
        from models.workout_history import WorkoutHistory

        plan = WorkoutPlan(
            user_id=1,
            goal="weight_loss",
            level="beginner",
            days=3,
            plan_json=json.dumps({"plan": []}),
        )
        db_session.add(plan)
        db_session.commit()

        history = WorkoutHistory(user_id=1, workout_id=plan.id, day=1, calories=100)
        db_session.add(history)
        db_session.commit()

        response = auth_client.post("/api/workouts/complete-day/1")
        assert response.status_code == 200
        assert response.json() == {"message": "Day 1 already completed"}

    def test_get_today_workout_success(self, auth_client, db_session):
        """Test getting today's workout."""

        from models.workout import WorkoutPlan

        plan = WorkoutPlan(
            user_id=1,
            goal="weight_loss",
            level="beginner",
            days=3,
            plan_json=json.dumps({"plan": []}),
        )
        db_session.add(plan)
        db_session.commit()

        response = auth_client.get("/api/workouts/today")
        assert response.status_code == 200

        data = response.json()
        assert data["day"] == 1
        assert "status" not in data

    def test_get_today_workout_completed_all(self, auth_client, db_session):
        """Test getting today's workout when all days are completed."""

        from models.workout import WorkoutPlan
        from models.workout_history import WorkoutHistory

        plan = WorkoutPlan(
            user_id=1,
            goal="weight_loss",
            level="beginner",
            days=2,
            plan_json=json.dumps({"plan": []}),
        )
        db_session.add(plan)
        db_session.commit()

        for day in [1, 2]:
            history = WorkoutHistory(
                user_id=1, workout_id=plan.id, day=day, calories=100
            )
            db_session.add(history)
        db_session.commit()

        response = auth_client.get("/api/workouts/today")
        assert response.status_code == 200

        data = response.json()
        assert data["status"] == "finished"
        assert "Workout plan completed" in data["message"]

    def test_get_today_workout_no_plan(self, auth_client):
        """Test getting today's workout when no plan exists."""
        response = auth_client.get("/api/workouts/today")
        assert response.status_code == 200
        assert response.json() == {"error": "No workout plan generated"}
