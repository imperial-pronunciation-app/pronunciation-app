from sqlmodel import SQLModel, create_engine
from app.models import Word, Phoneme, WordPhonemeLink

def test_create_database():
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False})
    SQLModel.metadata.create_all(engine)
    assert True
