from typing import Optional

import pytest
from fastapi.testclient import TestClient

from tests.utils import register_user


UPDATE_ENDPOINT = "/users/me"

def test_register_user(client: TestClient) -> None:
    """Should successfully register a user."""
    response = register_user(client)

    assert response.status_code == 201, f"Unexpected status: {response.status_code}, response: {response.json()}"

@pytest.mark.parametrize(
    "email, display_name, password, expected_status",
    [
        ("newuser@example.com", "New User", None, 422), # Missing password
        ("newuser@example.com", None, "password", 422), # Missing display name
        (None, "New User", "password", 422),            # Missing email
        (None, None, None, 422),                        # Missing all
    ]
)
def test_register_user_invalid_cases(client: TestClient, email: Optional[str], display_name: Optional[str], password: Optional[str], expected_status: int) -> None:
    """Should return correct status codes for invalid login attempts."""
    response = register_user(client, email=email, display_name=display_name, password=password)

    assert response.status_code == expected_status, f"Unexpected status: {response.status_code}, response: {response.json()}"

def test_update_user(auth_client: TestClient) -> None:
    """Should successfully update a user's email."""

    response = auth_client.patch(
        UPDATE_ENDPOINT,
        json={"email": "newemail@example.com"}
    )
    assert response.status_code == 200

def test_update_user_existing_email(client: TestClient, auth_client: TestClient) -> None:
    """Should return 401 when attempting to update user without a token."""
    email = "otheruser@example.com"
    register_user(client, email)

    response = auth_client.patch(
        UPDATE_ENDPOINT,
        json={"email": email}
    )
    assert response.status_code == 400
