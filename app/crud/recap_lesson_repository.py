
from typing import Optional

from sqlmodel import Session, select

from app.crud.generic_repository import GenericRepository
from app.models.recap_lesson import RecapLesson


class RecapLessonRepository(GenericRepository[RecapLesson]):

    def __init__(self, session: Session):
        super().__init__(session, RecapLesson)

    def find_recap_by_user_id_and_unit_id(self, user_id: int, unit_id: int) -> Optional[RecapLesson]:
        stmt = (
            select(RecapLesson)
            .where(RecapLesson.unit_id == unit_id, RecapLesson.user_id == user_id)
        )
        return self._session.exec(stmt).first()
