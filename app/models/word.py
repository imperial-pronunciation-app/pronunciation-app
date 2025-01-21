from typing import Optional, List, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship

from .word_phoneme_link import WordPhonemeLink
if TYPE_CHECKING:
    from .phoneme import Phoneme

# Possible words the user can pronounce
class Word(SQLModel, table = True):
    id: Optional[int] = Field(default = None, primary_key = True)
    word: str

    phonemes: List["Phoneme"] = Relationship(back_populates="words", link_model=WordPhonemeLink)