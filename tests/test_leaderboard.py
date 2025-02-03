from fastapi.testclient import TestClient
from sqlmodel import Session

from app.crud.unit_of_work import UnitOfWork
from app.models.leaderboard_user import LeaderboardUser, League
from app.models.user import User
from app.services.leaderboard import LeaderboardService
from app.services.user import UserService
from tests.utils import TEST_EMAIL, TEST_PASSWORD


def test_update_xp_existing_record(uow: UnitOfWork) -> None:
    # Pre
    user_id = 1
    league = League.GOLD
    xp_gain = 100

    # When
    result = uow.leaderboard_users.upsert(LeaderboardUser(user_id=user_id, league=league, xp=xp_gain))

    # Then
    assert result.user_id == user_id
    assert result.league == league
    assert result.xp == xp_gain

    # Pre
    user_service = UserService(uow)
    xp_gain = 50

    # When
    result2 = user_service.update_xp(user_id, xp_gain)

    # Then
    assert result2.user_id == user_id
    assert result2.league == league
    assert result2.xp == 150

    # When
    result3 = uow.leaderboard_users.get_by_user(user_id)

    # Then
    assert result3
    assert result3.user_id == user_id
    assert result3.league == league
    assert result3.xp == 150


def test_reset_leaderboard(authorised_client: TestClient, uow: UnitOfWork) -> None:
    # Pre
    user = uow.users.get_by_email(TEST_EMAIL)
    user_service = UserService(uow)
    user_service.update_xp(user.id, 10)
    assert uow.leaderboard_users.get_by_user(user.id).xp == 10

    # When
    leaderboard_service = LeaderboardService(uow)
    leaderboard_service.reset_leaderboard()
    response = authorised_client.get("/api/v1/leaderboard/global")

    # Then
    assert uow.leaderboard_users.get_by_user(user.id).xp == 0
    assert response.status_code == 200
    json = response.json()
    assert json["league"] == League.BRONZE
    assert json["leaders"] == [
        {"rank": 1, "username": TEST_EMAIL, "xp": 0},
    ]
    assert json["current"] == [{"rank": 0, "username": TEST_EMAIL, "xp": 0}]


def test_get_leaderboard_empty_user_record(session: Session, authorised_client: TestClient) -> None:
    leaders = [User(
        email=f"example{i}@gmail.com",
        hashed_password=TEST_PASSWORD,
        is_active=True,
        is_superuser=False,
        is_verified=True,
    ) for i in range(10)]
    session.add_all(leaders)
    session.flush()
    for i, leader in enumerate(leaders):
        session.refresh(leader)
        session.add(LeaderboardUser(user_id=leader.id, xp=i*2))
    
    response = authorised_client.get("/api/v1/leaderboard/global")
    assert response.status_code == 200
    json = response.json()
    assert json["league"] == League.BRONZE
    assert json["leaders"] == [
        {"rank": 1, "username": "example9@gmail.com", "xp": 18},
        {"rank": 2, "username": "example8@gmail.com", "xp": 16},
        {"rank": 3, "username": "example7@gmail.com", "xp": 14},
    ]
    assert json["current"] == [{"rank": 0, "username": TEST_EMAIL, "xp": 0}]
