from typing import TYPE_CHECKING, List

from sqlmodel import Relationship

from app.models.base.word_base import WordBase
from app.models.word_phoneme_link import WordPhonemeLink
from app.schemas.phoneme import PhonemePublic
from app.schemas.word import WordPublicWithPhonemes


if TYPE_CHECKING:
    from app.models.exercise import Exercise
    from app.models.phoneme import Phoneme

class Word(WordBase, table=True):
    phonemes: List["Phoneme"] = Relationship(back_populates="words", link_model=WordPhonemeLink)
    exercises: List["Exercise"] = Relationship(back_populates="word")

    def to_public_with_phonemes(self) -> WordPublicWithPhonemes:
        return WordPublicWithPhonemes(
            id=self.id,
            text=self.text,
            phonemes=[PhonemePublic(id=p.id, ipa=p.ipa, respelling=p.respelling) for p in self.phonemes]
        )
