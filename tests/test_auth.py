from typing import Optional

import pytest
from fastapi.testclient import TestClient

from app.models.user import User
from tests.utils import login_user


TEST_EMAIL = "newuser@example.com"
TEST_PASSWORD = "SecurePass123"

def test_login_user(client: TestClient, test_user: User) -> None:
    """Should successfully log in a registered user and return an access token."""
    response = login_user(client, test_user.email, "password")

    assert response.status_code == 200, f"Unexpected status: {response.status_code}, response: {response.json()}"
    assert "access_token" in response.json(), f"Response missing token: {response.json()}"

@pytest.mark.parametrize(
    "email, password, expected_status",
    [
        (TEST_EMAIL, "wrongPassword", 400),  # Wrong password
        (TEST_EMAIL, None, 422),             # Missing password
        (None, TEST_PASSWORD, 422),          # Missing username
        (None, None, 422),                   # Missing both
    ]
)
def test_login_user_invalid_cases(client: TestClient, email: Optional[str], password: Optional[str], expected_status: int) -> None:
    """Should return correct status codes for invalid login attempts."""
    response = login_user(client, email=email, password=password)

    assert response.status_code == expected_status, f"Unexpected status: {response.status_code}, response: {response.json()}"
