from typing import TYPE_CHECKING, List

from sqlmodel import Relationship

from app.models.base.word_base import WordBase
from app.models.word_phoneme_link import WordPhonemeLink


if TYPE_CHECKING:
    from app.models.phoneme import Phoneme

class Word(WordBase, table=True):
    phonemes: List["Phoneme"] = Relationship(back_populates="words", link_model=WordPhonemeLink)
