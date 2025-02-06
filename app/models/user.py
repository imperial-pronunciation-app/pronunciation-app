from typing import TYPE_CHECKING

from fastapi_users_db_sqlmodel import SQLModelBaseUserDB
from sqlmodel import Relationship

from app.models.id_model import IdModel
from app.models.leaderboard_user_link import LeaderboardUserLink


if TYPE_CHECKING:
    from app.models.leaderboard_user_link import LeaderboardUserLink

class User(IdModel, SQLModelBaseUserDB, table=True):
    leaderboard_entry: "LeaderboardUserLink" = Relationship(back_populates="user")
