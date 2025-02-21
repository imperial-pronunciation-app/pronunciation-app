from datetime import date as pydate
from datetime import datetime
from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship

from app.models.id_model import IdModel


if TYPE_CHECKING:
    from app.models.word import Word
    from app.models.word_of_day_attempt import WordOfDayAttempt


class WordOfDay(IdModel, table=True):
    id: int = Field(default=None, primary_key=True)
    word_id: int = Field(foreign_key="word.id")
    created_at: datetime = Field(default_factory=datetime.now)
    date: pydate = Field(index=True, default_factory=pydate.today)
    word: "Word" = Relationship(back_populates="word_of_day")
    word_of_day_attempts: List["WordOfDayAttempt"] = Relationship(back_populates="word_of_day", cascade_delete=True)
