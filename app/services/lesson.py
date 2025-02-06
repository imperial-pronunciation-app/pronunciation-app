from app.crud.unit_of_work import UnitOfWork
from app.models.lesson import Lesson
from app.models.user import User
from app.schemas.lesson import LessonResponse
from app.services.exercise import ExerciseService


class LessonService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow
    
    def to_response(self, lesson: Lesson, user: User) -> LessonResponse:
        return LessonResponse(
            title=lesson.title,
            is_completed=self._is_completed_by(lesson, user),
            first_exercise_id=lesson.exercises[0].id
        )
    
    def _is_completed_by(self, lesson: Lesson, user: User) -> bool:
        """Returns True if the user has completed this lesson. i.e. if all exercises were attempted"""
        exercise_service = ExerciseService(self._uow)
        return all(exercise_service.is_completed_by(exercise, user) for exercise in lesson.exercises)