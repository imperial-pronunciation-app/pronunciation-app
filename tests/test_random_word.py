import pytest
from fastapi.testclient import TestClient

# from app.main import app
# from app.models import Word, WordPhonemes, Phoneme
# from .conftest import engine

# client = TestClient(app)

def test_get_random_word(client: TestClient):
    response = client.get("/api/v1/random_word")
    assert response.status_code == 200
    data = response.json()

    # Test format of response
    assert "word_id" in data
    assert "word" in data
    assert "word_phonemes" in data
    assert isinstance(data["word_phonemes"], list)

    # Test content of response, given software and hardware seeded
    assert data["word"] in ["software", "hardware"]
    # TODO: Test phonemes
