from typing import TYPE_CHECKING

from fastapi_users_db_sqlmodel import SQLModelBaseUserDB
from sqlmodel import Relationship

from app.models.id_model import IdModel


if TYPE_CHECKING:
    from app.models.leaderboard_user import LeaderboardUser

class User(IdModel, SQLModelBaseUserDB, table=True):
    leaderboard_user: "LeaderboardUser" = Relationship(back_populates="user")
