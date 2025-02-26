from typing import Optional

from app.crud.unit_of_work import UnitOfWork
from app.models.lesson import Lesson
from app.models.user import User
from app.schemas.lesson import LessonResponse
from app.services.exercise import ExerciseService


class LessonService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow
    
    def to_response(self, lesson: Lesson, user: User, prev_lesson: Optional[Lesson] = None) -> LessonResponse:
        is_completed = self._is_completed_by(lesson, user)
        return LessonResponse(
            id=lesson.id,
            title=lesson.title,
            is_completed=is_completed,
            first_exercise_id=lesson.exercises[0].id,
            is_locked=prev_lesson is not None and not self._is_completed_by(prev_lesson, user),
            stars=self._stars_for(lesson, user) if is_completed else None
        )
    
    def _stars_for(self, lesson: Lesson, user: User) -> int:
        """Returns the number of stars (0 to 3) earned by the user for this lesson."""
        average_score = self._uow.exercise_attempts.average_max_score_for_lesson(user.id, lesson.id)
        if average_score >= 0.9:
            return 3
        elif average_score >= 0.7:
            return 2
        elif average_score >= 0.5:
            return 1
        else:
            return 0
    
    def _is_completed_by(self, lesson: Lesson, user: User) -> bool:
        """Returns True if the user has completed this lesson. i.e. if all exercises were attempted"""
        exercise_service = ExerciseService(self._uow)
        return all(exercise_service.is_completed_by(exercise, user) for exercise in lesson.exercises)
