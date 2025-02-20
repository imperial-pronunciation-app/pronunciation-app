# from fastapi.testclient import TestClient

# from app.models.exercise import Exercise


# def test_get_exercise_success(auth_client: TestClient, sample_exercise: Exercise) -> None:
#     """Test retrieving an exercise and ensuring phonemes are correctly included."""
#     exercise = sample_exercise
#     response = auth_client.get(f"/api/v1/exercises/{exercise.id}")

#     assert response.status_code == 200
#     data = response.json()

#     assert "word" in data
#     assert "phonemes" in data["word"]

#     assert data["word"]["phonemes"] == [{ "id": p.id, "ipa": p.ipa, "respelling": p.respelling } for p in exercise.word.phonemes]

#     assert "previous_exercise_id" in data
#     assert "next_exercise_id" in data

# def test_get_exercise_not_found(auth_client: TestClient) -> None:
#     """Test fetching an exercise that does not exist."""
#     response = auth_client.get("/api/v1/exercises/9999")  # ID that does not exist

#     assert response.status_code == 404
#     assert response.json()["detail"] == "Exercise not found"


# def test_get_exercise_unauthorized(client: TestClient, sample_exercise: Exercise) -> None:
#     """Test that unauthorized requests get a 401 error."""
#     response = client.get(f"/api/v1/exercises/{sample_exercise.id}")

#     assert response.status_code == 401
