from sqlmodel import Session, asc, select

from app.crud.generic_repository import GenericRepository
from app.models.word_of_day import WordOfDay


class WordOfDayRepository(GenericRepository[WordOfDay]):
    def __init__(self, session: Session):
        super().__init__(session, WordOfDay)

    # Get the latest word of the day
    def get_word_of_day(self) -> WordOfDay:
        stmt = select(WordOfDay).order_by(asc(WordOfDay.created_at)).limit(1)
        return self._session.exec(stmt).all()[0]
