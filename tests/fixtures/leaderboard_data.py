from typing import List, Sequence

import pytest
from fastapi.testclient import TestClient

from app.crud.unit_of_work import UnitOfWork
from app.models.leaderboard_user_link import LeaderboardUserLink, League
from app.models.user import User
from app.services.leaderboard import LeaderboardService
from app.services.user import UserService
from tests.utils import register_user


TEST_EMAILS = ["a@gmail.com", "b@gmail.com", "c@gmail.com", "d@gmail.com", "e@gmail.com"]
TEST_DISPLAY_NAMES = ["Alice", "Bob", "Charlie", "David", "Eve"]
TEST_XPS = [100, 80, 60, 40, 20]
TEST_EMAIL_TO_XP = dict(zip(TEST_EMAILS, TEST_XPS))


@pytest.fixture
def sample_users(client: TestClient, uow: UnitOfWork, emails: List[str] = TEST_EMAILS, display_names: List[str] = TEST_DISPLAY_NAMES) -> List[User]:
    """Sample users for testing the leaderboard, by default in bronze league and all with 0 xp."""
    for email, display_name in zip(emails, display_names):
        register_user(client, email, display_name)
    return [uow.users.get_by_email(email) for email in emails]


@pytest.fixture
def sample_leaderboard_users_no_xp(sample_users: List[User]) -> List[LeaderboardUserLink]:
    """Sample leaderboard users for testing the leaderboard, by default in bronze league and all with 0 xp."""
    return [user.leaderboard_entry for user in sample_users]


@pytest.fixture
def sample_leaderboard_users_bronze(uow: UnitOfWork, sample_leaderboard_users_no_xp: List[LeaderboardUserLink], xps: List[int] = TEST_XPS) -> List[LeaderboardUserLink]:
    """Sample leaderboard users in bronze league with xp."""
    user_service = UserService(uow)
    return [user_service.update_xp(u.user, xp) for u, xp in zip(sample_leaderboard_users_no_xp, xps)]

@pytest.fixture
def sample_leaderboard_users_silver(uow: UnitOfWork, sample_leaderboard_users_bronze: List[LeaderboardUserLink]) -> Sequence[LeaderboardUserLink]:
    """Sample leaderboard users in silver league with xp."""
    leaderboard_service = LeaderboardService(uow)
    return leaderboard_service.set_users_new_league(sample_leaderboard_users_bronze, League.SILVER)
