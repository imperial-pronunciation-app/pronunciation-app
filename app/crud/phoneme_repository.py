from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.generic_repository import GenericRepository
from app.models.phoneme import Phoneme
from app.models.word_phoneme_link import WordPhonemeLink


class PhonemeRepository(GenericRepository[Phoneme]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, Phoneme)
    
    async def find_phonemes_by_word(self, word_id: int) -> Sequence[Phoneme]:
        stmt = (
            select(Phoneme)
            .join(WordPhonemeLink)
            .where(WordPhonemeLink.word_id == word_id)
            .order_by(WordPhonemeLink.index)
        )
        return (await self._session.execute(stmt)).scalars().all()

    async def get_phoneme_by_ipa(self, ipa: str) -> Phoneme:
        return (await self._session.execute(select(Phoneme).where(Phoneme.ipa == ipa))).scalar_one()
