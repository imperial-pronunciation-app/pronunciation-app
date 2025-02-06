from typing import Sequence

from sqlmodel import Session, select

from app.crud.generic_repository import GenericRepository
from app.models.attempt import Attempt


class AttemptRepository(GenericRepository[Attempt]):

    def __init__(self, session: Session):
        super().__init__(session, Attempt)

    def find_by_user_id_and_exercise_id(self, user_id: int, exercise_id: int) -> Sequence[Attempt]:
        stmt = (
            select(Attempt)
            .where(Attempt.user_id == user_id, Attempt.exercise_id == exercise_id)
        )
        return self._session.exec(stmt).all()
