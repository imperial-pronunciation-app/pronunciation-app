from typing import Sequence

from sqlmodel import Session, col, func, select

from app.crud.generic_repository import GenericRepository
from app.models.attempt import Attempt
from app.models.exercise import Exercise
from app.models.exercise_attempt import ExerciseAttempt


class ExerciseAttemptRepository(GenericRepository[ExerciseAttempt]):
    def __init__(self, session: Session) -> None:
        super().__init__(session, ExerciseAttempt)
    
    def find_by_user_id_and_exercise_id(self, user_id: int, exercise_id: int) -> Sequence[ExerciseAttempt]:
        stmt = (
            select(ExerciseAttempt)
            .join(Attempt)
            .where(Attempt.user_id == user_id, ExerciseAttempt.exercise_id == exercise_id)
        )
        return self._session.exec(stmt).all()

    def get_max_score_by_user_id_and_exercise_id(self, user_id: int, exercise_id: int) -> int:
        return max([attempt.attempt.score for attempt in self.find_by_user_id_and_exercise_id(user_id, exercise_id)])
    
    def average_max_score_for_lesson(self, user_id: int, lesson_id: int) -> float:
        subquery = (
            select(
                ExerciseAttempt.exercise_id,
                func.max(Attempt.score).label("max_score")
            )
            .join(Exercise)
            .join(Attempt)
            .where(
                Attempt.user_id == user_id,
                Exercise.lesson_id == lesson_id
            )
            .group_by(col(ExerciseAttempt.exercise_id))
            .subquery()
        )

        return self._session.exec(
            select(func.avg(subquery.c.max_score))
        ).first() or 0.0
