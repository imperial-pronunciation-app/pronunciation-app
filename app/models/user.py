from datetime import date
from typing import TYPE_CHECKING

from fastapi_users_db_sqlmodel import SQLModelBaseUserDB
from sqlmodel import Field, Relationship

from app.models.id_model import IdModel
from app.models.leaderboard_user_link import LeaderboardUserLink


if TYPE_CHECKING:
    from app.models.leaderboard_user_link import LeaderboardUserLink

class User(IdModel, SQLModelBaseUserDB, table=True):
    login_streak: int = Field(default=1)
    last_login_date: date = Field(default_factory=date.today)
    xp_total: int = Field(default=0)
    level: int = Field(default=1)
    new_user: bool = Field(default=True)
    leaderboard_entry: "LeaderboardUserLink" = Relationship(back_populates="user")
