

from sqlmodel import Session

from app.crud.generic_repository import GenericRepository
from app.models.basic_lesson import BasicLesson


class BasicLessonRepository(GenericRepository[BasicLesson]):

    def __init__(self, session: Session):
        super().__init__(session, BasicLesson)

