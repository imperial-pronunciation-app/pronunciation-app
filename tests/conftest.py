import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, create_engine

from app.database import get_db
from app.main import app
from app.models import (  # noqa: F401
    ModelFeedback,
    Phoneme,
    Recording,
    RecordingFeedback,
    RecordingPhonemes,
    User,
    Word,
    WordPhonemes,
)
from app.seed import seed_data

DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "db")
DB_NAME = os.getenv("POSTGRES_TEST_DB", "test_db")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Override database dependency in app
def get_test_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = get_test_db


@pytest.fixture(scope="session", autouse=True)
def setup_db():
    SQLModel.metadata.create_all(engine)

    seed_data(DATABASE_URL)

    yield

    # Cleanup after tests
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as test_client:
        yield test_client
