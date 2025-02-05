from typing import List

from apscheduler.job import Job
from apscheduler.triggers.cron import CronTrigger
from fastapi.testclient import TestClient

from app.cron import scheduler, service
from app.crud.unit_of_work import UnitOfWork
from app.models.leaderboard_user import League
from app.models.user import User
from app.services.leaderboard import LeaderboardService
from app.services.user import UserService


def test_update_xp_existing_record(test_user: User, uow: UnitOfWork) -> None:
    # Pre
    user_service = UserService(uow)
    xp_gain = 50
    prev_league = test_user.leaderboard_user.league
    prev_xp = test_user.leaderboard_user.xp

    # When
    leaderboard_user = user_service.update_xp(test_user, xp_gain)

    # Then
    assert leaderboard_user.user_id == test_user.id
    assert leaderboard_user.league == prev_league
    assert leaderboard_user.xp == prev_xp + xp_gain


def test_reset_leaderboard(test_user: User, auth_client: TestClient, uow: UnitOfWork) -> None:
    # Pre
    user = test_user
    user_service = UserService(uow)
    user_service.update_xp(user, 10)
    assert test_user.leaderboard_user.xp == 10

    # When
    leaderboard_service = LeaderboardService(uow)
    leaderboard_service.reset_leaderboard()
    response = auth_client.get("/api/v1/leaderboard/global")

    # Then
    assert uow.leaderboard_users.get_by_user(user.id).xp == 0
    assert response.status_code == 200
    json = response.json()
    assert json["league"] == League.BRONZE
    assert json["leaders"] == [
        {"rank": 1, "username": test_user.email, "xp": 0},
    ]
    assert json["current"] == [{"rank": 0, "username": test_user.email, "xp": 0}]


def test_reset_leaderboard_cron_job_scheduled() -> None:
    jobs: List[Job] = scheduler.get_jobs()
    assert len(jobs) == 1
    job = jobs[0]
    assert job.func == service.reset_leaderboard
    assert job.trigger.__class__ == CronTrigger
