from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

from .word_phoneme_link import WordPhonemeLink


if TYPE_CHECKING:
    from .phoneme import Phoneme


# Possible words the user can pronounce
class Word(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    word: str

    phonemes: List["Phoneme"] = Relationship(back_populates="words", link_model=WordPhonemeLink)
