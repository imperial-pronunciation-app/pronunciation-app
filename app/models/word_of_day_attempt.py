from datetime import date, datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.id_model import IdModel


if TYPE_CHECKING:
    from app.models.word_of_day import WordOfDay


class WordOfDayAttempt(IdModel, table=True):
    word_of_day_id: int = Field(foreign_key="word.id")
    word_of_day: "WordOfDay" = Relationship(back_populates="word_of_day_attempt")
    user_id: int = Field(foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.now)
    attempt_date: date = Field(default_factory=date.today)
