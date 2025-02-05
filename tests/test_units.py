from typing import List

from fastapi.testclient import TestClient

from app.models.unit import Unit
from app.models.user import User


UNITS_ENDPOINT = "/api/v1/units"

def test_get_units_success(test_user: User, auth_client: TestClient, sample_units: List[Unit]) -> None:
    """Test retrieving units along with their lessons."""
    response = auth_client.get(UNITS_ENDPOINT)

    assert response.status_code == 200
    data = response.json()

    assert "units" in data

    # Validate the first unit
    unit_data = data["units"][0]
    unit = sample_units[0]
    assert unit_data["name"] == unit.name
    assert unit_data["description"] == unit.description
    
    # Validate the first lesson in the first unit
    assert "lessons" in unit_data
    lesson_data = unit_data["lessons"][0]
    lesson = unit.lessons[0]
    assert lesson_data["title"] == lesson.title
    assert lesson_data["first_exercise_id"] == lesson.exercises[0].id
    assert lesson_data["is_completed"] == lesson.is_completed(test_user)

def test_get_units_no_units(auth_client: TestClient) -> None:
    """Test retrieving units when there are none."""
    response = auth_client.get(UNITS_ENDPOINT)

    assert response.status_code == 200
    data = response.json()

    assert "units" in data
    assert len(data["units"]) == 0

def test_get_units_unauthorized(client: TestClient) -> None:
    """Test that unauthorized requests get a 401 error."""
    response = client.get(UNITS_ENDPOINT)

    assert response.status_code == 401
