

from fastapi.testclient import TestClient

from app.crud.unit_of_work import UnitOfWork
from app.services.unit import UnitService
from tests.factories.language import LanguageFactory
from tests.factories.unit import UnitFactory
from tests.factories.user import UserFactory


def units_endpoint(language: str) -> str:
    return f"/api/v1/{language}/units"

def test_get_units_success(auth_client: TestClient, make_unit: UnitFactory) -> None:
    """Test retrieving units along with their lessons."""
    unit = make_unit()
    response = auth_client.get(units_endpoint(unit.language.name))

    assert response.status_code == 200
    data = response.json()

    assert "units" in data

    # Validate the first unit
    unit_data = data["units"][0]
    assert unit_data["name"] == unit.name
    assert unit_data["description"] == unit.description

def test_get_units_no_units(auth_client: TestClient, make_language: LanguageFactory) -> None:
    """Test retrieving units when there are none."""
    language = make_language()
    response = auth_client.get(units_endpoint(language.name))

    assert response.status_code == 200
    data = response.json()

    assert "units" in data
    assert len(data["units"]) == 0

def test_get_units_unauthorized(client: TestClient, make_language: LanguageFactory) -> None:
    """Test that unauthorized requests get a 401 error."""
    language = make_language()
    response = client.get(units_endpoint(language.name))

    assert response.status_code == 401

def test_generate_recap_lesson(
    uow: UnitOfWork,
    make_user: UserFactory,
    make_unit: UnitFactory
    ) -> None:
    user = make_user()
    unit = make_unit()
    service = UnitService(uow)
    service.generate_recap_lesson(unit, user)
    
    recap = uow.recap_lessons.find_recap_by_user_id_and_unit_id(user.id, unit.id)
    assert recap is not None