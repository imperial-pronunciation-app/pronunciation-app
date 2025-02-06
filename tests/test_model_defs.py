from sqlmodel import SQLModel, create_engine

from app.models import Attempt, Exercise, Lesson, Phoneme, Recording, Unit, Word, WordPhonemeLink  # noqa: F401


def test_create_database() -> None:
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    assert True
