from typing import List

from app.crud.unit_of_work import UnitOfWork
from app.models.phoneme import Phoneme
from app.schemas.phoneme import PhonemePublic


class PhonemeService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def get_public_phonemes(self, phoneme_strings: List[str]) -> List[PhonemePublic]:
        return [self._to_phoneme_public(await self._uow.phonemes.get_phoneme_by_ipa(ipa)) for ipa in phoneme_strings]

    def _to_phoneme_public(self, phoneme: Phoneme) -> PhonemePublic:
        return PhonemePublic(
            id=phoneme.id,
            ipa=phoneme.ipa,
            respelling=phoneme.respelling
        )