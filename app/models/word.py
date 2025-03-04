from datetime import date, datetime
from typing import TYPE_CHECKING, List

from sqlmodel import Field, Relationship

from app.models.base.word_base import WordBase
from app.models.word_phoneme_link import WordPhonemeLink


if TYPE_CHECKING:
    from app.models.exercise import Exercise
    from app.models.language import Language
    from app.models.phoneme import Phoneme
    from app.models.word_of_day import WordOfDay


class Word(WordBase, table=True):
    phonemes: List["Phoneme"] = Relationship(
        back_populates="words", link_model=WordPhonemeLink, sa_relationship_kwargs={"order_by": "WordPhonemeLink.index"}
    )
    exercises: List["Exercise"] = Relationship(back_populates="word")
    word_of_day: List["WordOfDay"] = Relationship(back_populates="word")
    word_of_day_last_used: date = Field(default=datetime.min.date())
    language_id: int = Field(foreign_key="language.id")
    language: "Language" = Relationship(back_populates="words")
