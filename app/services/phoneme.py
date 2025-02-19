
from app.crud.unit_of_work import UnitOfWork
from app.schemas.phoneme import PhonemePublic


class PhonemeService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def to_phoneme_public(self, phoneme_str: str) -> PhonemePublic:
        phoneme = self._uow.phonemes.get_phoneme_by_ipa(phoneme_str)
        return PhonemePublic(
            id=phoneme.id,
            ipa=phoneme.ipa,
            respelling=phoneme.respelling
        )