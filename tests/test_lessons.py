from typing import List

from fastapi.testclient import TestClient

from app.models.exercise import Exercise
from app.models.lesson import Lesson


def test_get_lesson_success(auth_client: TestClient, sample_exercises: List[Exercise]) -> None:
    """Test retrieving an lesson and ensuring phonemes are correctly included."""
    lesson = sample_exercises[0].lesson
    response = auth_client.get(f"/api/v1/lessons/{lesson.id}")

    assert response.status_code == 200
    data = response.json()

    assert "exercises" in data
    assert data["current_exercise_index"] == 0

    assert data["exercises"][0]["word"]["phonemes"] == [{ "id": p.id, "ipa": p.ipa, "respelling": p.respelling } for p in lesson.exercises[0].word.phonemes]


def test_get_lesson_not_found(auth_client: TestClient) -> None:
    """Test fetching an lesson that does not exist."""
    response = auth_client.get("/api/v1/lessons/9999")  # ID that does not exist

    assert response.status_code == 404
    assert response.json()["detail"] == "Lesson not found"


def test_get_lesson_unauthorized(client: TestClient, sample_lesson: Lesson) -> None:
    """Test that unauthorized requests get a 401 error."""
    response = client.get(f"/api/v1/lessons/{sample_lesson.id}")

    assert response.status_code == 401
