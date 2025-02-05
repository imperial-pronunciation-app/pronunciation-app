
from sqlmodel import Session

from app.crud.generic_repository import GenericRepository
from app.models.lesson import Lesson


class LessonRepository(GenericRepository[Lesson]):

    def __init__(self, session: Session):
        super().__init__(session, Lesson)

    