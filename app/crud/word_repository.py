from datetime import date, timedelta
from random import choice

from sqlmodel import Session, select

from app.crud.generic_repository import GenericRepository
from app.models.word import Word


class WordRepository(GenericRepository[Word]):
    def __init__(self, session: Session):
        super().__init__(session, Word)

    def get_word_not_used_for(self, days: int) -> Word:
        stmt = select(Word).where(Word.word_of_day_last_used < date.today() - timedelta(days=days))
        res_list = self._session.exec(stmt)
        res = choice(list(res_list))
        res.word_of_day_last_used = date.today()
        self.upsert(res)
        return res
