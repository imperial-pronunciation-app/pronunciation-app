
from app.crud.unit_of_work import UnitOfWork
from app.models.phoneme import Phoneme
from app.schemas.phoneme import PhonemePublic


class PhonemeService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def to_phoneme_public(self, phoneme: Phoneme, language_id: int) -> PhonemePublic:
        return PhonemePublic(
            id=phoneme.id,
            ipa=phoneme.ipa,
            cdn_path=phoneme.cdn_path,
            respelling=next(r for r in phoneme.respellings if r.language_id == language_id).respelling
        )