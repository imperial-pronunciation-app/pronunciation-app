from contextlib import asynccontextmanager
from typing import AsyncGenerator

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from sqlmodel import Session

from app.crud.unit_of_work import UnitOfWork
from app.database import engine
from app.services.leaderboard import LeaderboardService
from app.services.user import UserService
from app.services.word_of_day import WordOfDayService


def _daily_cron_callback() -> None:
    with Session(engine) as session, UnitOfWork(session) as uow:
        WordOfDayService(uow).change_word_of_day()
        UserService(uow).disable_new_user_boost()


def _weekly_cron_callback() -> None:
    with Session(engine) as session, UnitOfWork(session) as uow:
        LeaderboardService(uow).reset_leaderboard()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Before app startup
    scheduler = BackgroundScheduler()
    scheduler.add_job(_daily_cron_callback, "cron", hour=0, timezone="UTC")
    scheduler.add_job(_weekly_cron_callback, "cron", day_of_week="sun", hour=0, timezone="UTC")
    scheduler.start()
    yield

    # After app shutdown
    scheduler.shutdown()
