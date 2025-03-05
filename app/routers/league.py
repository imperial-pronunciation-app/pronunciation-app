from fastapi import APIRouter, Depends

from app.models.user import User
from app.users import current_active_user


router = APIRouter()


@router.get("/api/v1/league", response_model=str)
async def get_units(user: User = Depends(current_active_user)) -> str:
    return user.leaderboard_entry.league
