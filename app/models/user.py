from typing import List

from fastapi_users_db_sqlmodel import SQLModelBaseUserDB
from sqlmodel import Relationship

from app.models.id_model import IdModel
from app.models.leaderboard_user import LeaderboardUser


class User(IdModel, SQLModelBaseUserDB, table=True):
    leaderboard_users: List[LeaderboardUser] = Relationship(back_populates="user")
