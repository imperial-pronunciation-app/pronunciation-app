import math
from typing import List

from apscheduler.job import Job
from apscheduler.triggers.cron import CronTrigger
from fastapi.testclient import TestClient

from app.cron import scheduler, service
from app.crud.unit_of_work import UnitOfWork
from app.models.leaderboard_user_link import LeaderboardUserLink, League
from app.redis import LRedis
from app.services.leaderboard import LeaderboardService
from app.services.user import UserService
from tests.utils import TEST_DOMAIN, TEST_EMAIL, TEST_USERNAME, register_users


def test_update_xp_existing_record(uow: UnitOfWork) -> None:
    # Pre
    user_id = 1
    league = League.GOLD
    xp_gain = 100

    # When
    result = uow.leaderboard_users.upsert(LeaderboardUserLink(user_id=user_id, league=league, xp=xp_gain))

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
    assert result3.user_id == user_id
    assert result3.league == league
    assert result3.xp == 150


def test_reset_leaderboard(authorised_client: TestClient, uow: UnitOfWork) -> None:
    # Pre
    initial_xp = 10
    user = uow.users.get_by_email(TEST_EMAIL)
    user_service = UserService(uow)
    user_service.update_xp(user.id, initial_xp)
    assert user.leaderboard_users[0].xp == initial_xp

    # When
    leaderboard_service = LeaderboardService(uow)
    leaderboard_service.reset_leaderboard()
    response = authorised_client.get("/api/v1/leaderboard/global")

    # Then
    expected_xp = int(math.log2(initial_xp + 1))
    assert user.leaderboard_users[0].xp == expected_xp
    assert response.status_code == 200
    json = response.json()
    assert json["league"] == League.SILVER # Promotion
    assert json["leaders"] == [
        {"rank": 1, "username": TEST_EMAIL, "xp": expected_xp},
    ]
    assert json["user_position"] == [{"rank": 1, "username": TEST_EMAIL, "xp": expected_xp}]


def test_get_leaderboard_empty_user_record(authorised_client: TestClient, uow: UnitOfWork) -> None:
    # Pre
    user_service = UserService(uow)
    register_users(authorised_client)
    leaders = uow.users.all()
    for leader in leaders:
        user_service.update_xp(leader.id, leader.id * 2)

    # When
    response = authorised_client.get("/api/v1/leaderboard/global")

    # Then
    assert response.status_code == 200
    json = response.json()
    assert json["league"] == League.BRONZE
    assert json["leaders"] == [
        {"rank": 1, "username": f"{TEST_USERNAME}9@{TEST_DOMAIN}", "xp": 22},
        {"rank": 2, "username": f"{TEST_USERNAME}8@{TEST_DOMAIN}", "xp": 20},
        {"rank": 3, "username": f"{TEST_USERNAME}7@{TEST_DOMAIN}", "xp": 18},
    ]
    assert json["user_position"] == [
        {"rank": 9, "username": f"{TEST_USERNAME}1@{TEST_DOMAIN}", "xp": 6},
        {"rank": 10, "username": f"{TEST_USERNAME}0@{TEST_DOMAIN}", "xp": 4},
        {"rank": 11, "username": TEST_EMAIL, "xp": 2},
    ]


def test_reset_leaderboard_cron_job_scheduled() -> None:
    jobs: List[Job] = scheduler.get_jobs()
    assert len(jobs) == 1
    job = jobs[0]
    assert job.func == service.reset_leaderboard
    assert job.trigger.__class__ == CronTrigger


def test_promotion_demotion(authorised_client: TestClient, uow: UnitOfWork) -> None:
    # Pre: test with silver league for both promotions and demotions
    register_users(authorised_client, count=4)
    user_service = UserService(uow)
    leaderboard_service = LeaderboardService(uow)
    leaderboard_service.set_users_new_league(uow.leaderboard_users.all(), League.SILVER)
    LRedis.move_all_entries(League.BRONZE, League.SILVER)
    users = uow.users.all()
    for user in users:
        user_service.update_xp(user.id, user.id ** 2 * 200)

    # When
    original_order = uow.leaderboard_users.find_by_league_order_by_xp_desc_with_limit(League.SILVER, 5)
    leaderboard_service.reset_leaderboard()

    # Then
    leaderboard_users = uow.leaderboard_users.all()
    gold = [user for user in leaderboard_users if user.league == League.GOLD]
    silver = sorted([user for user in leaderboard_users if user.league == League.SILVER], key=lambda x: x.xp, reverse=True)
    bronze = [user for user in leaderboard_users if user.league == League.BRONZE]

    assert len(gold) == 1
    assert len(silver) == 3
    assert len(bronze) == 1
    assert gold[0].xp >= silver[0].xp
    assert bronze[0].xp <= silver[2].xp
    assert original_order[0].id == gold[0].id
    assert original_order[1].id == silver[0].id
    assert original_order[2].id == silver[1].id
    assert original_order[3].id == silver[2].id
    assert original_order[4].id == bronze[0].id
