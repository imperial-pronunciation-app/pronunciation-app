from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, func
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
    user_id: UUID = Field(foreign_key="user.id", index=True)
    league: League = Field(sa_column=Column(SQLEnum(League), index=True))
    xp: int = Field(default=0)
    created_at: datetime = Field(default=datetime.now)
    updated_at: datetime = Field(default=datetime.now, sa_column=Column(DateTime, default=datetime.now, onupdate=func.now()))

# Create composite index if queries filter on all columns simultaneously
