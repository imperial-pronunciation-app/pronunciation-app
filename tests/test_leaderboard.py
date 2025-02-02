from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.leaderboard_user import LeaderboardUser, League
from app.models.user import User
from tests.utils import TEST_EMAIL, TEST_PASSWORD


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
