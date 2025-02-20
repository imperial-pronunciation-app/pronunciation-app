from typing import AsyncGenerator, Iterator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.pool import StaticPool

from app.crud.unit_of_work import UnitOfWork
from app.database import get_async_session
from app.main import app
from app.models.base_model import Base
from app.models.user import User
from app.redis import LRedis

from .utils import login_user, register_user


pytest_plugins = [
   "tests.fixtures.curriculum_data",
   "tests.fixtures.leaderboard_data",
]

@pytest_asyncio.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    """Yields an in-memory database session
    """
    engine = create_async_engine("sqlite+aiosqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as session:
        yield session


@pytest.fixture
def client(session: AsyncSession) -> Iterator[TestClient]:
    """Yields a TestClient with an in-memory database session override
    """
    def get_session_override() -> AsyncSession:
        return session

    app.dependency_overrides[get_async_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(session: AsyncSession, client: TestClient) -> User:
    email = "test@example.com"
    register_user(client, email, "password")
    return (await session.execute(select(User).filter(User.email == email))).scalar_one() # type: ignore


@pytest_asyncio.fixture
async def auth_client(client: TestClient, test_user: User) -> TestClient:
    """Returns a TestClient with a seeded user token
    """
    user_token = login_user(client, test_user.email, "password").json()["access_token"]
    client.headers.update({"Authorization": f"Bearer {user_token}"})
    return client


@pytest.fixture
def uow(session: AsyncSession) -> Iterator[UnitOfWork]:
    """Returns a UnitOfWork instance
    """
    with UnitOfWork(session) as uow:
        yield uow


@pytest.fixture(autouse=True)
def reset_redis() -> Iterator[None]:
    """Reset redis after each test
    """
    yield
    LRedis.clear()
