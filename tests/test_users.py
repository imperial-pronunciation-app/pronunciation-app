from fastapi.testclient import TestClient
from httpx import Response


TEST_EMAIL = "newuser@example.com"
TEST_PASSWORD = "SecurePass123"
REGISTER_ENDPOINT = "/auth/register"
LOGIN_ENDPOINT = "/auth/jwt/login"

def register_user(client: TestClient) -> Response:
    """Helper function to create a new user for testing."""
    return client.post(REGISTER_ENDPOINT, json={"email": TEST_EMAIL, "password": TEST_PASSWORD})

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
    response = client.post(REGISTER_ENDPOINT, json={"email": TEST_EMAIL})  # Missing password
    assert response.status_code == 422

def test_login_user(client: TestClient) -> None:
    """Should successfully log in a registered user and return an access token."""
    register_user(client)
    response = client.post(LOGIN_ENDPOINT, data={"username": TEST_EMAIL, "password": TEST_PASSWORD})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_user_bad_credentials(client: TestClient) -> None:
    """Should return 400 when logging in with incorrect credentials."""
    register_user(client)
    response = client.post(LOGIN_ENDPOINT, data={"username": TEST_EMAIL, "password": "wrongPassword"})
    assert response.status_code == 400

def test_login_user_missing_details(client: TestClient) -> None:
    """Should return 422 when missing required login details."""
    register_user(client)
    response = client.post(LOGIN_ENDPOINT, data={"username": TEST_EMAIL})  # Missing password
    assert response.status_code == 422
