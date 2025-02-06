from typing import Optional

from fastapi.testclient import TestClient
from httpx import Response


TEST_EMAIL = "newuser@example.com"
TEST_PASSWORD = "SecurePass123"
REGISTER_ENDPOINT = "/users/register"
LOGIN_ENDPOINT = "/auth/jwt/login"

def register_user(client: TestClient, email: Optional[str] = TEST_EMAIL, password: Optional[str] = TEST_PASSWORD) -> Response:
    """Helper function to create a new user for testing."""
    body = {}
    if email:
        body["email"] = email
    if password:
        body["password"] = password

    return client.post(REGISTER_ENDPOINT, json=body)

def login_user(client: TestClient, email: Optional[str] = TEST_EMAIL, password: Optional[str] = TEST_PASSWORD) -> Response:
    """Helper function to log in a user for testing."""
    body = {}
    if email:
        body["username"] = email
    if password:
        body["password"] = password

    return client.post(LOGIN_ENDPOINT, data=body)
