from fastapi.testclient import TestClient

from tests.utils import login_user, register_user


def test_login_user(client: TestClient) -> None:
    """Should successfully log in a registered user and return an access token."""
    register_user(client)
    response = login_user(client)

    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_user_bad_credentials(client: TestClient) -> None:
    """Should return 400 when logging in with incorrect credentials."""
    register_user(client)
    response = login_user(client, password="wrongPassword")
    assert response.status_code == 400

def test_login_user_missing_details(client: TestClient) -> None:
    """Should return 422 when missing required login details."""
    register_user(client)
    response = login_user(client, password=None)
    assert response.status_code == 422
