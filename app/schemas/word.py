from typing import List

from app.models.base.word_base import WordBase
from app.schemas.phoneme import PhonemePublic


class WordPublicWithPhonemes(WordBase):
    phonemes: List[PhonemePublic]
