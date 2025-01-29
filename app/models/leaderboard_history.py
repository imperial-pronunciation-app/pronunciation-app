from datetime import date
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Column
from sqlmodel import Enum as SQLEnum
from sqlmodel import Field, SQLModel

from app.models.leaderboard import League


if TYPE_CHECKING:
    pass


class LeaderboardHistory(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id", index=True)
    league: League = Field(sa_column=Column(SQLEnum(League), index=True))
    xp: int = Field(default=0)
    rank: int = Field(index=True)
    week_end: date = Field(default=date.today, index=True)

# Create composite index if queries filter on all columns simultaneously
