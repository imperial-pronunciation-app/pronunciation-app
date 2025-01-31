from fastapi.testclient import TestClient

from tests.utils import login_user, register_user


UPDATE_ENDPOINT = "/users/me"

def test_register_user(client: TestClient) -> None:
    """Should successfully register a new user."""
    response = register_user(client)
    assert response.status_code == 201

def test_register_user_existing_email(client: TestClient) -> None:
    """Should return 400 when registering a user with an existing email."""
    register_user(client)  # Register the user once
    response = register_user(client)  # Attempt to register again
    assert response.status_code == 400

def test_register_user_missing_details(client: TestClient) -> None:
    """Should return 422 when missing required fields in registration."""
    response = register_user(client, password=None)  # Missing password
    assert response.status_code == 422

def test_update_user(client: TestClient) -> None:
    """Should successfully update a user's email."""
    register_user(client)

    token = login_user(client).json()["access_token"]

    response = client.patch(
        UPDATE_ENDPOINT,
        json={"email": "newemail@example.com"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200

def test_update_user_missing_token(client: TestClient) -> None:
    """Should return 401 when attempting to update user without a token."""
    register_user(client)

    response = client.patch(
        UPDATE_ENDPOINT,
        json={"email": "newemail@example.com"}
    )
    assert response.status_code == 401

def test_update_user_existing_email(client: TestClient) -> None:
    """Should return 401 when attempting to update user without a token."""
    register_user(client)
    email = "otheruser@example.com"
    register_user(client, email)

    token = login_user(client).json()["access_token"]

    response = client.patch(
        UPDATE_ENDPOINT,
        json={"email": email},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400
