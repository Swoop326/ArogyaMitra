import pytest
from unittest.mock import patch, MagicMock


class TestNutritionRoutes:
    """Test cases for nutrition routes."""

    @patch("services.nutrition_service.generate_nutrition_plan")
    @patch("routes.nutrition.find_recipe")
    def test_generate_plan_success(self, mock_find_recipe, mock_generate_plan, client):
        """Test successful nutrition plan generation."""
        # Mock the service response
        mock_plan = {
            "weeklyPlan": [
                {"day": "Monday", "meals": ["Oatmeal", "Chicken Salad", "Rice"]}
            ]
        }
        mock_generate_plan.return_value = mock_plan

        # Mock recipe finding
        mock_find_recipe.return_value = {"recipe_id": 123, "image": "test_image.jpg"}

        plan_data = {"calories": 2000, "diet": "balanced", "allergies": "none"}

        with patch("routes.nutrition.datetime") as mock_datetime:
            mock_datetime.today.return_value.strftime.return_value = "Monday"

            response = client.post("/api/nutrition/plan", json=plan_data)
            assert response.status_code == 200

            data = response.json()
            assert "weeklyPlan" in data
            assert len(data["weeklyPlan"]) == 1
            assert data["weeklyPlan"][0]["day"] == "Monday"

    @patch("routes.nutrition.requests.get")
    def test_get_recipes_success(self, mock_get, client):
        """Test getting random recipes."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "recipes": [
                {
                    "id": 1,
                    "title": "Test Recipe",
                    "image": "test.jpg",
                    "readyInMinutes": 30,
                    "servings": 4,
                }
            ]
        }
        mock_get.return_value = mock_response

        response = client.get("/api/nutrition/recipes?diet=vegetarian")
        assert response.status_code == 200

        data = response.json()
        assert len(data) == 1
        assert data[0]["title"] == "Test Recipe"
        assert data[0]["id"] == 1

    @patch("routes.nutrition.requests.get")
    def test_get_recipes_api_error(self, mock_get, client):
        """Test recipes endpoint when API fails."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        response = client.get("/api/nutrition/recipes")
        assert response.status_code == 200
        assert response.json() == {"error": "Spoonacular API failed"}

    @patch("routes.nutrition.requests.get")
    def test_get_recipe_details_success(self, mock_get, client):
        """Test getting recipe details."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "title": "Test Recipe",
            "image": "test.jpg",
            "readyInMinutes": 30,
            "servings": 4,
            "summary": "A test recipe",
            "instructions": "Mix ingredients",
            "extendedIngredients": [
                {"original": "1 cup flour"},
                {"original": "2 eggs"},
            ],
        }
        mock_get.return_value = mock_response

        response = client.get("/api/nutrition/recipe/123")
        assert response.status_code == 200

        data = response.json()
        assert data["title"] == "Test Recipe"
        assert data["readyInMinutes"] == 30
        assert len(data["ingredients"]) == 2
        assert "1 cup flour" in data["ingredients"]

    @patch("routes.nutrition.requests.get")
    def test_get_recipe_details_api_error(self, mock_get, client):
        """Test recipe details when API fails."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        response = client.get("/api/nutrition/recipe/123")
        assert response.status_code == 200
        assert response.json() == {"error": "Recipe fetch failed"}


class TestNutritionHelpers:
    """Test cases for nutrition helper functions."""

    @patch("routes.nutrition.requests.get")
    def test_find_recipe_success(self, mock_get):
        """Test successful recipe finding."""
        from routes.nutrition import find_recipe

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "results": [{"id": 456, "image": "recipe.jpg"}]
        }
        mock_get.return_value = mock_response

        result = find_recipe("Chicken Curry")
        assert result is not None
        assert result["recipe_id"] == 456
        assert result["image"] == "recipe.jpg"

    @patch("routes.nutrition.requests.get")
    def test_find_recipe_no_results(self, mock_get):
        """Test recipe finding when no results."""
        from routes.nutrition import find_recipe

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"results": []}
        mock_get.return_value = mock_response

        result = find_recipe("Unknown Meal")
        assert result is None

    @patch("routes.nutrition.requests.get")
    def test_find_recipe_api_limit(self, mock_get):
        """Test recipe finding when API limit reached."""
        from routes.nutrition import find_recipe

        mock_response = MagicMock()
        mock_response.status_code = 402
        mock_get.return_value = mock_response

        result = find_recipe("Chicken Curry")
        assert result is None

    @patch("routes.nutrition.requests.get")
    def test_find_recipe_exception(self, mock_get):
        """Test recipe finding when exception occurs."""
        from routes.nutrition import find_recipe

        mock_get.side_effect = Exception("Network error")

        result = find_recipe("Chicken Curry")
        assert result is None
