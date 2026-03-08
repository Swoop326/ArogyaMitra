from services.ai_service import ai_coach_response


def test_ai_coach_response():

    response = ai_coach_response("I feel tired")

    assert "AROMI AI Coach says" in response["reply"]
