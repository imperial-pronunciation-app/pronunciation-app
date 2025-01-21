from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

from .word_phoneme_link import WordPhonemeLink


if TYPE_CHECKING:
    from .word import Word


# Possible phoneme in each words
# ipa is the International Phonetic Alphabet representation of the phoneme
# respelling is a common respelling of the phoneme (wiki respelling)
class Phoneme(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    ipa: str
    respelling: str

    # words: List["Word"] = Relationship(back_populates="phonemes", link_model=WordPhonemeLink)
    words: List["Word"] = Relationship(link_model=WordPhonemeLink)
