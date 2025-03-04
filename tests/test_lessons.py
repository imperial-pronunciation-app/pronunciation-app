
from fastapi.testclient import TestClient

from tests.factories.lesson import LessonFactory


def test_get_lesson_success(auth_client: TestClient, make_lesson: LessonFactory) -> None:
    """Test fetching an lesson that exists."""
    lesson = make_lesson()
    response = auth_client.get(f"/api/v1/lessons/{lesson.id}")

    assert response.status_code == 200
    data = response.json()

    assert "exercise_ids" in data
    assert data["current_exercise_index"] == 0

def test_get_lesson_not_found(auth_client: TestClient) -> None:
    """Test fetching an lesson that does not exist."""
    response = auth_client.get("/api/v1/lessons/9999")  # ID that does not exist

    assert response.status_code == 404
    assert response.json()["detail"] == "Lesson not found"


def test_get_lesson_unauthorized(client: TestClient, make_lesson: LessonFactory) -> None:
    """Test that unauthorized requests get a 401 error."""
    lesson = make_lesson()
    response = client.get(f"/api/v1/lessons/{lesson.id}")

    assert response.status_code == 401
