from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from .phoneme import Phoneme
from .word import Word


class WordPhonemes(SQLModel, table=True):
    word_id: Optional[int] = Field(foreign_key="word.id", primary_key=True)
    phoneme_id: Optional[int] = Field(foreign_key="phoneme.id", primary_key=True)
    index: int

    word: Optional["Word"] = Relationship(back_populates="phonemes")
    phoneme: Optional["Phoneme"] = Relationship(back_populates="words")
