from app.crud.unit_of_work import UnitOfWork
from app.models.basic_lesson import BasicLesson
from app.models.lesson import Lesson
from app.models.recap_lesson import RecapLesson
from app.models.user import User
from app.schemas.lesson import LessonResponse
from app.services.exercise import ExerciseService


class LessonService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def basic_to_response(self, basic: BasicLesson, user: User) -> LessonResponse:
        lesson = self._uow.lessons.get_by_id(basic.id)
        return self.to_response(lesson, user)
    
    def recap_to_response(self, recap: RecapLesson, user: User) -> LessonResponse:
        lesson = self._uow.lessons.get_by_id(recap.id)
        return self.to_response(lesson, user)
    
    def to_response(self, lesson: Lesson, user: User) -> LessonResponse:
        return LessonResponse(
            id=lesson.id,
            title=lesson.title,
            is_completed=self._is_completed_by(lesson, user),
            first_exercise_id=lesson.exercises[0].id
        )
    
    def _is_completed_by(self, lesson: Lesson, user: User) -> bool:
        """Returns True if the user has completed this lesson. i.e. if all exercises were attempted"""
        exercise_service = ExerciseService(self._uow)
        return all(exercise_service.is_completed_by(exercise, user) for exercise in lesson.exercises)

    def _is_last_lesson(self, lesson: BasicLesson) -> bool:
        """Returns True if this is the last lesson within the unit."""
        return lesson.index == len(lesson.unit.lessons) - 1