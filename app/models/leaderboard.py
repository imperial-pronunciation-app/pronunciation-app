from datetime import date, datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, Index
from sqlalchemy import Enum as SQLEnum
from sqlmodel import Field, SQLModel


if TYPE_CHECKING:
    pass


class League(str, Enum):
    GOLD = "Gold"
    SILVER = "Silver"
    BRONZE = "Bronze"

class Leaderboard(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(index=True)
    # user_id: UUID = Field(foreign_key="user.id", index=True)
    league: League = Field(sa_column=Column(SQLEnum(League), index=True))
    xp: int = Field(default=0)
    current: bool = Field(default=True, index=True)
    rank: Optional[int] = Field(default=None, index=True)
    week_end: Optional[date] = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column=Column(DateTime, default=datetime.now, onupdate=datetime.now))

    __table_args__ = (
        Index("idx__leaderboard__user_id__league__current__rank__week_end", "user_id", "league", "current", "rank", "week_end"),
    )

# Create composite index if queries filter on all columns simultaneously
