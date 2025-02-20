from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, relationship

from app.models.base.word_base import WordBase


if TYPE_CHECKING:
    from app.models.exercise import Exercise
    from app.models.phoneme import Phoneme

class Word(WordBase):
    __tablename__ = "word"

    phonemes: Mapped[List["Phoneme"]] = relationship(back_populates="words", secondary="word_phoneme_link", order_by="WordPhonemeLink.index")
    exercises: Mapped[List["Exercise"]] = relationship(back_populates="word")