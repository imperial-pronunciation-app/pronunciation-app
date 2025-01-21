

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import Word


def test_read_random_word(session: Session, client: TestClient) -> None:
    word = Word(word="software")
    session.add(word)
    session.commit()

    response = client.get("/api/v1/random_word")

    data = response.json()
    assert response.status_code == 200
    assert data["word"] == "software"