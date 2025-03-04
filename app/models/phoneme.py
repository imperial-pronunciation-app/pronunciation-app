from typing import TYPE_CHECKING, List

from sqlmodel import Relationship

from app.models.base.phoneme_base import PhonemeBase

from .word_phoneme_link import WordPhonemeLink


if TYPE_CHECKING:
    from app.models.phoneme_respelling import PhonemeRespelling

    from .word import Word

class Phoneme(PhonemeBase, table=True):
    words: List["Word"] = Relationship(back_populates="phonemes", link_model=WordPhonemeLink)
    respellings: List["PhonemeRespelling"] = Relationship(back_populates="phoneme")
