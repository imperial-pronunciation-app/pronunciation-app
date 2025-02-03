from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import Depends

from app.crud.unit_of_work import UnitOfWork, get_unit_of_work
from app.services.leaderboard import LeaderboardService


uow: UnitOfWork = Depends(get_unit_of_work)
service = LeaderboardService(uow)

scheduler = BackgroundScheduler()
scheduler.add_job(service.reset_leaderboard, "cron", day_of_week="sun", hour=0, minute=0, timezone="UTC")
