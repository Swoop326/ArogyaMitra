import pytest
from unittest.mock import patch, MagicMock
from services.ai_service import ai_coach_response
from services.workout_service import generate_workout_plan
from services.nutrition_service import generate_nutrition_plan
from services.analytics_service import calculate_bmi, calculate_bmr


class TestAIService:
    """Test cases for AI service."""

    def test_ai_coach_response(self):
        """Test AI coach response."""
        message = "How to stay motivated?"
        response = ai_coach_response(message)

        assert isinstance(response, dict)
        assert "reply" in response
        assert "AROMI AI Coach says:" in response["reply"]
        assert message in response["reply"]


class TestWorkoutService:
    """Test cases for workout service."""

    @patch("services.workout_service.client")
    def test_generate_workout_plan_success(self, mock_client):
        """Test successful workout plan generation."""
        # Mock the Groq client response
        mock_response = MagicMock()
        mock_response.choices[0].message.content = """
        {
          "plan": [
            {
              "day": "Day 1",
              "workout": "Upper Body Strength",
              "exercises": [
                {
                  "name": "Push-ups",
                  "sets": 3,
                  "reps": 10,
                  "description": "Standard push-ups"
                }
              ]
            }
          ]
        }
        """
        mock_client.chat.completions.create.return_value = mock_response

        result = generate_workout_plan("weight_loss", "beginner", 3)

        assert isinstance(result, dict)
        assert "plan" in result
        assert len(result["plan"]) == 1
        assert result["plan"][0]["day"] == "Day 1"
        assert result["plan"][0]["workout"] == "Upper Body Strength"

    @patch("services.workout_service.client")
    def test_generate_workout_plan_with_health_profile(self, mock_client):
        """Test workout plan generation with health profile."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = '{"plan": []}'
        mock_client.chat.completions.create.return_value = mock_response

        # Mock health profile
        health_profile = MagicMock()
        health_profile.heart_conditions = "None"
        health_profile.diabetes = "No"
        health_profile.blood_pressure = "Normal"
        health_profile.knee_injury = "No"
        health_profile.back_pain = "Mild"
        health_profile.other_injuries = "None"

        # Mock body metrics
        body_metrics = MagicMock()
        body_metrics.height = 170
        body_metrics.weight = 70
        body_metrics.bmi = 24.2

        result = generate_workout_plan(
            "weight_loss", "beginner", 3, health_profile, body_metrics
        )

        # Verify the API was called with health context
        mock_client.chat.completions.create.assert_called_once()
        call_args = mock_client.chat.completions.create.call_args
        prompt = call_args[1]["messages"][0]["content"]

        assert "Medical conditions: None" in prompt
        assert "Height: 170 cm" in prompt
        assert "Weight: 70 kg" in prompt
        assert "BMI: 24.2" in prompt


class TestNutritionService:
    """Test cases for nutrition service."""

    @patch("services.nutrition_service.client")
    def test_generate_nutrition_plan_success(self, mock_client):
        """Test successful nutrition plan generation."""
        mock_response = MagicMock()
        mock_response.choices[0].message.content = """
        {
          "meals": [
            {
              "meal": "Breakfast",
              "food": "Oatmeal with fruits",
              "calories": 300
            }
          ]
        }
        """
        mock_client.chat.completions.create.return_value = mock_response

        result = generate_nutrition_plan("weight_loss", 2000)

        assert isinstance(result, dict)
        assert "meals" in result
        assert len(result["meals"]) == 1
        assert result["meals"][0]["meal"] == "Breakfast"


class TestAnalyticsService:
    """Test cases for analytics service."""

    def test_calculate_bmi(self):
        """Test BMI calculation."""
        # Test normal BMI
        bmi = calculate_bmi(70, 1.75)  # 70kg, 175cm
        assert round(bmi, 1) == 22.9

        # Test underweight
        bmi = calculate_bmi(50, 1.75)
        assert round(bmi, 1) == 16.3

        # Test overweight
        bmi = calculate_bmi(90, 1.75)
        assert round(bmi, 1) == 29.4

    def test_calculate_bmi_edge_cases(self):
        """Test BMI calculation edge cases."""
        # Zero height should raise error
        with pytest.raises(ZeroDivisionError):
            calculate_bmi(70, 0)

        # Negative values
        with pytest.raises(ValueError):
            calculate_bmi(-70, 1.75)

        with pytest.raises(ValueError):
            calculate_bmi(70, -1.75)

    def test_calculate_bmr_harris_benedict(self):
        """Test BMR calculation using Harris-Benedict equation."""
        # Male: BMR = 88.362 + (13.397 × weight in kg) + (4.799 × height in cm) - (5.677 × age in years)
        # Female: BMR = 447.593 + (9.247 × weight in kg) + (3.098 × height in cm) - (4.330 × age in years)

        # Test male
        bmr_male = calculate_bmr(70, 175, 25, "male")
        expected_male = 88.362 + (13.397 * 70) + (4.799 * 175) - (5.677 * 25)
        assert round(bmr_male, 1) == round(expected_male, 1)

        # Test female
        bmr_female = calculate_bmr(60, 165, 25, "female")
        expected_female = 447.593 + (9.247 * 60) + (3.098 * 165) - (4.330 * 25)
        assert round(bmr_female, 1) == round(expected_female, 1)

    def test_calculate_bmr_invalid_gender(self):
        """Test BMR calculation with invalid gender."""
        with pytest.raises(ValueError):
            calculate_bmr(70, 175, 25, "other")

    def test_calculate_bmr_edge_cases(self):
        """Test BMR calculation edge cases."""
        # Zero or negative values
        with pytest.raises(ValueError):
            calculate_bmr(0, 175, 25, "male")

        with pytest.raises(ValueError):
            calculate_bmr(70, 0, 25, "male")

        with pytest.raises(ValueError):
            calculate_bmr(70, 175, 0, "male")
