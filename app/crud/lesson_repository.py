
from typing import Optional

from sqlmodel import Session, select

from app.crud.generic_repository import GenericRepository
from app.models.lesson import Lesson


class LessonRepository(GenericRepository[Lesson]):

    def __init__(self, session: Session):
        super().__init__(session, Lesson)

    def find_recap_by_user_id_and_unit_id(self, unit_id: int, user_id: int) -> Optional[Lesson]:
        stmt = (
            select(Lesson)
            .where(Lesson.unit_id == unit_id, Lesson.user_id == user_id)
        )
        return self._session.exec(stmt).first()

    