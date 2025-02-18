from fastapi.testclient import TestClient

from app.models.word_of_day import WordOfDay


def test_get_word_of_day(auth_client: TestClient, sample_word_of_day: WordOfDay) -> None:
    """Test retrieving the word of the day with corresponding phonemes."""

    # When
    word_of_day = sample_word_of_day
    assert word_of_day.id is not None
    response = auth_client.get("/api/v1/word_of_day")

    # Then
    assert response.status_code == 200
    data = response.json()
    assert data["text"] == word_of_day.word.text
    assert data["id"] == word_of_day.word_id
    assert data["phonemes"] == [
        {"id": p.id, "ipa": p.ipa, "respelling": p.respelling} for p in word_of_day.word.phonemes
    ]


def test_get_new_word_unauthorized(client: TestClient) -> None:
    """Test that unauthorized requests get a 401 error."""

    # When
    response = client.get("/api/v1/word_of_day")

    # Then
    assert response.status_code == 401
