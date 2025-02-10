from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship

from app.models.id_model import IdModel


if TYPE_CHECKING:
    from app.models.word import Word


class WordOfDay(IdModel, table=True):
    word_id: int = Field(foreign_key="word.id")
    created_at: datetime = Field(default_factory=datetime.now)
    word: "Word" = Relationship(back_populates="word_of_day")
