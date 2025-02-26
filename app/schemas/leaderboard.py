from dataclasses import dataclass
from typing import List

from pydantic import BaseModel

from app.models.leaderboard_user_link import League


@dataclass
class LeaderboardEntry:
    rank: int
    display_name: str
    xp: int


class LeaderboardResponse(BaseModel):
    league: League
    days_until_end: int
    leaders: List[LeaderboardEntry]
    user_position: List[LeaderboardEntry]
