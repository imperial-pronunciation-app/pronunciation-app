from datetime import date, timedelta

from sqlmodel import Session, select

from app.crud.generic_repository import GenericRepository
from app.models.word import Word


class WordRepository(GenericRepository[Word]):
    def __init__(self, session: Session):
        super().__init__(session, Word)

    def get_word_not_used_for(self, days: int) -> Word:
        # TODO: Should this be done atomically?
        stmt = select(Word).where(Word.word_of_day_last_used < date.today() - timedelta(days=days))
        res = self._session.exec(stmt).one()
        res.word_of_day_last_used = date.today()
        self.upsert(res)
        return res
