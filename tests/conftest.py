from typing import Iterator

import pytest
from fastapi.testclient import TestClient
from httpx import Headers
from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool

from app.crud.unit_of_work import UnitOfWork
from app.database import get_session
from app.main import app
from app.models.user import User
from app.redis import LRedis

from .utils import login_user, register_user


pytest_plugins = [
    "tests.factories.language",
    "tests.factories.phoneme",
    "tests.factories.user",
    "tests.factories.word",
    "tests.factories.leaderboard_user",
    "tests.factories.unit",
    "tests.factories.basic_lesson",
    "tests.factories.lesson",
    "tests.factories.exercise",
    "tests.factories.exercise_attempt",
    "tests.factories.word_of_day"
]


@pytest.fixture
def session() -> Iterator[Session]:
    """Yields an in-memory database session"""
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session


@pytest.fixture
def client(session: Session) -> Iterator[TestClient]:
    """Yields a TestClient with an in-memory database session override"""

    def get_session_override() -> Session:
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture
def test_user(session: Session, client: TestClient) -> User:
    email = "test@example.com"
    display_name = "Test User"
    register_user(client, email, display_name, "password")
    return session.exec(select(User).where(User.email == email)).one()


@pytest.fixture
def auth_client(client: TestClient, test_user: User) -> TestClient:
    """Returns a TestClient with a seeded user token"""
    user_token = login_user(client, test_user.email, "password").json()["access_token"]
    client.headers = Headers({"Authorization": f"Bearer {user_token}"})
    return client


@pytest.fixture
def uow(session: Session) -> Iterator[UnitOfWork]:
    """Returns a UnitOfWork instance"""
    with UnitOfWork(session) as uow:
        yield uow


@pytest.fixture(autouse=True)
def reset_redis() -> Iterator[None]:
    """Reset redis after each test"""
    yield
    LRedis.clear()
