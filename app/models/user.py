from datetime import date
from typing import TYPE_CHECKING

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.id_model import IdModel


if TYPE_CHECKING:
    from app.models.leaderboard_user_link import LeaderboardUserLink

class User(IdModel, SQLAlchemyBaseUserTable[Mapped[int]]):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    login_streak: Mapped[int] = mapped_column(Integer, default=1)
    last_login_date: Mapped[date] = mapped_column(Date, default=date.today)
    xp_total: Mapped[int] = mapped_column(Integer, default=0)
    level: Mapped[int] = mapped_column(Integer, default=1)
    new_user: Mapped[bool] = mapped_column(Boolean, default=True)
    leaderboard_entry: Mapped["LeaderboardUserLink"] = relationship(back_populates="user")

    created_at: Mapped[date] = mapped_column(Date, default=date.today)