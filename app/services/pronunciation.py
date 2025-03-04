from typing import List, Optional, Tuple

from app.crud.unit_of_work import UnitOfWork
from app.models.word import Word
from app.schemas.aligned_phonemes import AlignedPhonemes
from app.services.phoneme import PhonemeService
from app.utils.compute_alignment import compute_alignment
from app.utils.phoneme_similarity import phoneme_similarity


class PronunciationService:
    """Service for phoneme alignment and pronunciation scoring."""

    def __init__(self, uow: UnitOfWork, deletion_penalty: float = -1.0, insertion_penalty: float = -0.5):
        self._uow = uow
        self.deletion_penalty = deletion_penalty
        self.insertion_penalty = insertion_penalty

    def evaluate_pronunciation(
        self, word: Word, pronounced_phonemes: List[str]
    ) -> Tuple[AlignedPhonemes, int]:
        """
        Aligns phonemes and scores pronunciation based on phoneme similarity.

        :param word: Attempted word.
        :param pronounced_phonemes: List of user-pronounced phonemes.
        :return: Tuple of aligned phonemes and a pronunciation score (0-100).
        """
        expected = list(map(lambda x: x.ipa, self._uow.phonemes.find_phonemes_by_word(word.id)))
        alignment, score = compute_alignment(expected, pronounced_phonemes, phoneme_similarity, self.deletion_penalty, self.insertion_penalty)

        return self.convert_alignment_to_phoneme_public(alignment, word.language_id), score
    
    def convert_alignment_to_phoneme_public(
        self, alignment: List[Tuple[Optional[str], Optional[str]]], language_id: int
    ) -> AlignedPhonemes:
        phoneme_service = PhonemeService(self._uow)
        return [
            (
                phoneme_service.to_phoneme_public(
                    self._uow.phonemes.get_phoneme_by_ipa(exp), language_id
                ) if exp else None,
                phoneme_service.to_phoneme_public(
                    self._uow.phonemes.get_phoneme_by_ipa(act), language_id
                ) if act else None
            )
            for exp, act in alignment
        ]