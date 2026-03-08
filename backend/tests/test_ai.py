def test_aromi_chat(client):

    response = client.post("/api/ai/aromi-chat")

    assert response.status_code == 200
    assert "response" in response.json()


def test_chat_with_aromi(client):

    payload = {"message": "Give me a workout"}

    response = client.post("/api/ai/chat", json=payload)

    assert response.status_code == 200
    assert "reply" in response.json()
