from sqlmodel import Session

from app.crud.generic_repository import GenericRepository
from app.models.word_of_day_attempt import WordOfDayAttempt


class WordOfDayAttemptRepository(GenericRepository[WordOfDayAttempt]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, WordOfDayAttempt)
