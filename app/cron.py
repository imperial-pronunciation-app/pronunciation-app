from contextlib import asynccontextmanager
from typing import AsyncGenerator, Callable

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import Depends, FastAPI

from app.crud.unit_of_work import UnitOfWork, get_unit_of_work
from app.services.leaderboard import LeaderboardService
from app.services.user import UserService
from app.services.word_of_day import WordOfDayService


class ParrotCron:
    """Cron job scheduler for Parrot backend. Non-generic on purpose."""

    def __init__(self) -> None:
        self._scheduler = BackgroundScheduler()
        self._add_daily_job(self._disable_new_user_boost_wrapper)
        self._add_daily_job(self._change_word_of_day_wrapper)
        self._add_weekly_job(self._reset_leaderboard_wrapper)

    def start(self) -> None:
        self._scheduler.start()

    def shutdown(self) -> None:
        self._scheduler.shutdown()
    
    def _add_daily_job(self, callback: Callable[[UnitOfWork], None]) -> None:
        self._scheduler.add_job(callback, "cron", hour=0, timezone="UTC")
    
    def _add_weekly_job(self, callback: Callable[[UnitOfWork], None]) -> None:
        self._scheduler.add_job(callback, "cron", day_of_week="sun", hour=0, timezone="UTC")

    @staticmethod
    def _disable_new_user_boost_wrapper(uow: UnitOfWork = Depends(get_unit_of_work)) -> None:
        UserService(uow).disable_new_user_boost()

    @staticmethod
    def _change_word_of_day_wrapper(uow: UnitOfWork = Depends(get_unit_of_work)) -> None:
        WordOfDayService(uow).change_word_of_day()

    @staticmethod
    def _reset_leaderboard_wrapper(uow: UnitOfWork = Depends(get_unit_of_work)) -> None:
        LeaderboardService(uow).reset_leaderboard()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Before app startup
    cron = ParrotCron()
    cron.start()
    yield

    # After app shutdown
    cron.shutdown()
