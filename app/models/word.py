from typing import TYPE_CHECKING, List

from sqlmodel import Relationship

from app.models.id_model import IdModel
from app.models.word_phoneme_link import WordPhonemeLink


if TYPE_CHECKING:
    from app.models.phoneme import Phoneme


# Possible words the user can pronounce
class Word(IdModel, table=True):
    word: str

    phonemes: List["Phoneme"] = Relationship(back_populates="words", link_model=WordPhonemeLink)
