from datetime import date

from sqlmodel import Session, select

from app.crud.generic_repository import GenericRepository
from app.crud.word_repository import WordRepository
from app.models.word import Word
from app.models.word_of_day import WordOfDay


class WordOfDayRepository(GenericRepository[WordOfDay]):
    def __init__(self, session: Session):
        super().__init__(session, WordOfDay)

    def get_word_of_day(self) -> WordOfDay:
        stmt = select(WordOfDay).where(WordOfDay.date == date.today())
        return self._session.exec(stmt).one()

    def add_word_of_day(self, word_id: int) -> None:
        word_of_day = WordOfDay(word_id=word_id, date=date.today())
        # Also update the last used date of the word
        stmt = select(Word).where(Word.id == word_id)
        word = self._session.exec(stmt).one()
        word.word_of_day_last_used = date.today()
        WordRepository(self._session).upsert(word)
        self.upsert(word_of_day)
