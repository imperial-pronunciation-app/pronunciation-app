from typing import List

from fastapi.testclient import TestClient

from app.models.word import Word


CONTINUAL_PRACTICE_ENDPOINT = "/api/v1/continual_practice"

def test_get_continual_practice_word_success(auth_client: TestClient, sample_words: List[Word]) -> None:
    """Test getting a random word """
    response = auth_client.get(CONTINUAL_PRACTICE_ENDPOINT)

    assert response.status_code == 200
    data = response.json()

    assert "phonemes" in data
    assert "text" in data

    # Check that the returned word is in sample_words
    assert data["text"] in map(lambda w: w.text, sample_words)

def test_continual_practice_no_words(auth_client: TestClient) -> None:
    """Test getting a random word when there are none."""
    response = auth_client.get(CONTINUAL_PRACTICE_ENDPOINT)

    assert response.status_code == 503

def test_get_continual_practice_unauthorized(client: TestClient) -> None:
    """Test that unauthorized requests get a 401 error."""
    response = client.get(CONTINUAL_PRACTICE_ENDPOINT)

    assert response.status_code == 401
