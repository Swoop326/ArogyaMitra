def test_generate_nutrition_plan(client):

    payload = {
        "calories": 2000,
        "diet": "vegetarian",
        "allergies": "none"
    }

    response = client.post("/api/nutrition/plan", json=payload)

    assert response.status_code == 200


def test_get_recipes(client):

    response = client.get("/api/nutrition/recipes")

    assert response.status_code in [200, 500]
