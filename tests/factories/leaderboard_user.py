from typing import List, Optional, Protocol, TypedDict

import pytest

from app.crud.unit_of_work import UnitOfWork
from app.models.leaderboard_user_link import LeaderboardUserLink, League
from app.services.leaderboard import LeaderboardService
from app.services.user import UserService
from tests.factories.language import LanguageFactory
from tests.factories.user import UserFactory


class UserDetails(TypedDict):
    email: str
    display_name: str
    xp: int

DEFAULT_USER_DETAILS: List[UserDetails] = [
    {"email": "a@gmail.com", "display_name": "Alice", "xp": 100},
    {"email": "b@gmail.com", "display_name": "Bob", "xp": 80},
    {"email": "c@gmail.com", "display_name": "Charlie", "xp": 60},
    {"email": "d@gmail.com", "display_name": "David", "xp": 40},
    {"email": "e@gmail.com", "display_name": "Eve", "xp": 20}
]

class LeaderboardUsersFactory(Protocol):
    def __call__(self, user_details: List[UserDetails] = DEFAULT_USER_DETAILS, league: Optional[League] = None, create_language: bool = True) -> List[LeaderboardUserLink]:
        ...

@pytest.fixture
def make_leaderboard_users(uow: UnitOfWork, make_user: UserFactory, make_language: LanguageFactory) -> LeaderboardUsersFactory:
    def make(user_details: List[UserDetails] = DEFAULT_USER_DETAILS, league: Optional[League] = None, create_language: bool = True) -> List[LeaderboardUserLink]:
        if create_language:
            make_language()
        user_service = UserService(uow)
        leaderboard_users = []

        for user_detail in user_details:
            user = make_user(email=user_detail["email"], display_name=user_detail["display_name"], create_language=False)
            leaderboard_users.append(user_service.update_xp(user, user_detail["xp"]))

        if league:
            leaderboard_service = LeaderboardService(uow)
            return list(leaderboard_service.set_users_new_league(leaderboard_users, league))
        
        return leaderboard_users
    return make
