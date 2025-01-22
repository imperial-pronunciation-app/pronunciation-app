from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.database import get_session
from app.main import app
from app.seed import SeedData, WordData, seed_data


@pytest.fixture(name="session")
def session_fixture() -> Iterator[Session]:
    """Yields an in-memory database session
    """
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Iterator[TestClient]:
    """Yields a TestClient with an in-memory database session override
    """
    def get_session_override() -> Session:
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture
def test_seed_data(request: pytest.FixtureRequest) -> SeedData:
    """Default test data to seed a test database with
    """
    return getattr(request, "param", SeedData(words=[
        WordData(word="software", phonemes=["s", "oʊ", "f", "t", "w", "ɛ", "r"]),
        WordData(word="hardware", phonemes=["h", "ɑː", "r", "d", "w", "ɛ", "r"]),
    ]))
    
@pytest.fixture(name="seeded_session")
def seeded_session_fixture(session: Session, test_seed_data: SeedData) -> Iterator[Session]:
    """Yields an in-memory database session seeded with test data
    """
    seed_data(session, seed_words=test_seed_data)
    yield session

@pytest.fixture(name="seeded_client")
def seeded_client_fixture(seeded_session: Session) -> Iterator[TestClient]:
    """Yields a TestClient with an in-memory database session seeded with test data
    """
    def get_session_override() -> Session:
        return seeded_session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()
