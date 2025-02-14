import random

from app.crud.unit_of_work import UnitOfWork
from app.models.word import Word
from app.schemas.phoneme import PhonemePublic
from app.schemas.word import WordPublicWithPhonemes


class WordService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow
        
    def to_public_with_phonemes(self, word: Word) -> WordPublicWithPhonemes:
        return WordPublicWithPhonemes(
            id=word.id,
            text=word.text,
            phonemes=[PhonemePublic(id=p.id, ipa=p.ipa, respelling=p.respelling) for p in word.phonemes]
        )

    def get_random(self) -> Word:
        words = self._uow.words.all()
        if len(words) == 0:
            raise IndexError("No words to choose from")
        return random.choice(words)