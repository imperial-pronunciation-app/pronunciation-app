from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING

from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SQLEnum
from sqlmodel import Field

from app.models.base_model import BaseModel


if TYPE_CHECKING:
    pass


class League(str, Enum):
    GOLD = "Gold"
    SILVER = "Silver"
    BRONZE = "Bronze"


class LeaderboardUser(BaseModel, table=True):
    user_id: int = Field(foreign_key="user.id", index=True)
    league: League = Field(sa_column=Column(SQLEnum(League), index=True))
    xp: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now, sa_column=Column(DateTime, default=datetime.now, onupdate=datetime.now))
