from fastapi import APIRouter, Depends

from app.crud.unit_of_work import UnitOfWork, get_unit_of_work
from app.models.user import User
from app.schemas.leaderboard import LeaderboardResponse
from app.services.leaderboard import LeaderboardService
from app.users import current_active_user


router = APIRouter()

@router.get("/api/v1/leaderboard/global")
async def get_leaderboard(
    uow: UnitOfWork = Depends(get_unit_of_work),
    user: User = Depends(current_active_user),
) -> LeaderboardResponse:
    service = LeaderboardService(uow)
    return service.get_global_leaderboard_for_user(user)
