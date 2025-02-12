from fastapi.testclient import TestClient

from app.models.word_of_day import WordOfDay


def test_get_word_of_day(auth_client: TestClient, sample_word_of_day: WordOfDay) -> None:
    """Test retrieving the word of the day with corresponding phonemes."""
    word_of_day = sample_word_of_day
    assert word_of_day.id is not None
    response = auth_client.get("/api/v1/word_of_day")

    assert response.status_code == 200
    data = response.json()

    assert "word" in data
    assert "id" in data
    assert "phonemes" in data["word"]
    assert "id" in data["word"]
    assert "text" in data["word"]
