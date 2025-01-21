import pytest
from fastapi.testclient import TestClient

from app.seed import SeedData, WordData


def test_read_random_word_empty(client: TestClient) -> None:
    """Test that random_word endpoint returns 404 for an empty table

    Args:
        session (Session): Session for unseeded database
        client (TestClient): TestClient for FastAPI
    """

    response = client.get("/api/v1/random_word")

    assert response.status_code == 404

@pytest.mark.parametrize("test_seed_data", [
    SeedData(words=[
        WordData(word="software", phonemes=["s", "oʊ", "f", "t", "w", "ɛ", "r"]),
    ]),
    SeedData(words=[
        WordData(word="hardware", phonemes=["h", "ɑː", "r", "d", "w", "ɛ", "r"]),
    ])
], indirect=True)
def test_read_random_word_single(seeded_client: TestClient, test_seed_data: SeedData) -> None:
    """Test that random_word endpoint returns a single word from a seeded table

    Args:
        seeded_client (TestClient): _description_
        test_seed_data (SeedData): _description_
    """
    response = seeded_client.get("/api/v1/random_word")
    data = response.json()
    assert response.status_code == 200
    assert data["word"] == test_seed_data.words[0].word
    # turn on once endpoint also returns phonemes
    # assert data["word_phonemes"] == test_seed_data.words[0].phonemes