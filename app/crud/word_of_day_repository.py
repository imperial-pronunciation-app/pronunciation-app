from datetime import date

from sqlmodel import Session, select

from app.crud.generic_repository import GenericRepository
from app.models.word_of_day import WordOfDay


class WordOfDayRepository(GenericRepository[WordOfDay]):
    def __init__(self, session: Session):
        super().__init__(session, WordOfDay)

    # Get the latest word of the day
    def get_word_of_day(self) -> WordOfDay:
        stmt = select(WordOfDay).where(WordOfDay.date == date.today())
        return self._session.exec(stmt).one()
