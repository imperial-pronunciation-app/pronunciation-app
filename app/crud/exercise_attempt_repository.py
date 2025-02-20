from typing import Sequence

from sqlmodel import Session, select

from app.crud.generic_repository import GenericRepository
from app.models.exercise_attempt import ExerciseAttempt


class ExerciseAttemptRepository(GenericRepository[ExerciseAttempt]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, ExerciseAttempt)
    
    def find_by_user_id_and_exercise_id(self, user_id: int, exercise_id: int) -> Sequence[ExerciseAttempt]:
        stmt = (
            select(ExerciseAttempt)
            .where(ExerciseAttempt.attempt.user_id == user_id, ExerciseAttempt.exercise_id == exercise_id)
        )
        return self._session.exec(stmt).all()