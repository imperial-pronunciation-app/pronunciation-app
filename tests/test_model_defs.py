from sqlmodel import SQLModel, create_engine

from app.models import (  # noqa: F401
    Attempt,
    Exercise,
    LeaderboardUserLink,
    Lesson,
    Phoneme,
    Recording,
    Unit,
    User,
    Word,
    WordPhonemeLink,
)


def test_create_database() -> None:
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    assert True
