# from typing import TYPE_CHECKING, List

# from sqlmodel import Relationship

# from app.models.base.phoneme_base import PhonemeBase

# from .word_phoneme_link import WordPhonemeLink


# if TYPE_CHECKING:
#     from .word import Word

# # Possible phoneme in each words
# # ipa is the International Phonetic Alphabet representation of the phoneme
# # respelling is a common respelling of the phoneme (wiki respelling)
# class Phoneme(PhonemeBase, table=True):
#     words: List["Word"] = Relationship(back_populates="phonemes", link_model=WordPhonemeLink)

from typing import TYPE_CHECKING, List

from sqlalchemy.orm import Mapped, relationship

from app.models.base.phoneme_base import PhonemeBase


if TYPE_CHECKING:
    from app.models.word import Word

class Phoneme(PhonemeBase):
    __tablename__ = "phoneme"
    
    words: Mapped[List["Word"]] = relationship(back_populates="phonemes", secondary="word_phoneme_link")