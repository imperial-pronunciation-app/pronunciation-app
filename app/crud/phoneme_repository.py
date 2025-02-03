from typing import Sequence

from sqlmodel import Session, col, select

from app.crud.generic_repository import GenericRepository
from app.models.phoneme import Phoneme
from app.models.word_phoneme_link import WordPhonemeLink


class PhonemeRepository(GenericRepository[Phoneme]):

    def __init__(self, session: Session):
        super().__init__(session, Phoneme)
    
    def find_phonemes_by_word(self, word_id: int) -> Sequence[Phoneme]:
        stmt = (
            select(Phoneme)
            .join(WordPhonemeLink)
            .where(WordPhonemeLink.word_id == word_id)
            .order_by(col(WordPhonemeLink.index))
        )
        return self._session.exec(stmt).all()

    def get_phoneme_by_ipa(self, ipa: str) -> Phoneme:
        phoneme = self._session.exec(select(Phoneme).where(Phoneme.ipa == ipa)).one()
        return phoneme
