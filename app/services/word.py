from typing import List

from app.crud.unit_of_work import UnitOfWork
from app.models.word import Word
from app.schemas.word import WordPublicWithPhonemes
from app.services.phoneme import PhonemeService


class WordService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow
    
    def word_similarity(self, word: Word, attempt: List[str]) -> int:
        attempt_str = " ".join(attempt)

        return self._edit_distance(word.text, attempt_str)

    
    def _edit_distance(self, word1: str, word2: str) -> int:
        m = len(word1)
        n = len(word2)

        # Stores dp[i-1][j-1]
        prev = 0
        curr = [0] * (n + 1)

        for j in range(n + 1):
            curr[j] = j

        for i in range(1, m + 1):
            prev = curr[0]
            curr[0] = i
            for j in range(1, n + 1):
                temp = curr[j]
                if word1[i - 1] == word2[j - 1]:
                    curr[j] = prev
                else:
                    curr[j] = 1 + min(curr[j - 1], prev, curr[j])
                prev = temp

        return curr[n]
        
        
    def to_public_with_phonemes(self, word: Word) -> WordPublicWithPhonemes:
        phoneme_service = PhonemeService(self._uow)
        return WordPublicWithPhonemes(
            id=word.id,
            text=word.text,
            phonemes=[phoneme_service.to_phoneme_public(p, word.language_id) for p in word.phonemes]
        )