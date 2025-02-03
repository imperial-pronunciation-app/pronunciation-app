from typing import List, Optional

from fastapi.testclient import TestClient
from httpx import Response


TEST_USERNAME = "newuser"
TEST_DOMAIN = "example.com"
TEST_EMAIL = f"{TEST_USERNAME}@{TEST_DOMAIN}"
TEST_PASSWORD = "SecurePass123"
REGISTER_ENDPOINT = "/users/register"
LOGIN_ENDPOINT = "/auth/jwt/login"

def register_user(client: TestClient, email: str = TEST_EMAIL, password: Optional[str] = TEST_PASSWORD) -> Response:
    """Helper function to create a new user for testing."""
    body = {}
    if email:
        body["email"] = email
    if password:
        body["password"] = password

    return client.post(REGISTER_ENDPOINT, json=body)


def register_users(client: TestClient, count: int = 10, username_base: str = TEST_USERNAME, domain: str = TEST_DOMAIN, password: Optional[str] = TEST_PASSWORD) -> List[Response]:
    """Helper function to create multiple new users for testing."""
    responses = []
    for i in range(count):
        email = f"{username_base}{i}@{domain}"
        responses.append(register_user(client, email, password))
    return responses


def login_user(client: TestClient, email: str = TEST_EMAIL, password: Optional[str] = TEST_PASSWORD) -> Response:
    """Helper function to log in a user for testing."""
    body = {}
    if email:
        body["username"] = email
    if password:
        body["password"] = password

    return client.post(LOGIN_ENDPOINT, data=body)