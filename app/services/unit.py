from app.crud.unit_of_work import UnitOfWork
from app.models.exercise import Exercise
from app.models.lesson import Lesson
from app.models.recap_lesson import RecapLesson
from app.models.unit import Unit
from app.models.user import User
from app.schemas.unit import UnitPublicWithLessons
from app.services.basic_lesson import BasicLessonService
from app.services.lesson import LessonService
from app.services.recap_lesson import RecapLessonService


class UnitService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow
    
    def to_public_with_lessons(self, unit: Unit, user: User) -> UnitPublicWithLessons:
        basic_lesson_service = BasicLessonService(self._uow)
        recap_lesson_service = RecapLessonService(self._uow)
        recap_lesson = self._uow.recap_lessons.find_recap_by_user_id_and_unit_id(user.id, unit.id)

        is_locked = not (unit.index == 0 or self._is_completed_by(self._uow.units.all_ordered()[unit.index - 1], user))

        return UnitPublicWithLessons(
            id=unit.id,
            name=unit.name,
            description=unit.description,
            lessons=[basic_lesson_service.to_response(lesson, user) for lesson in unit.lessons] if not is_locked else None,
            recap_lesson=recap_lesson_service.to_response(recap_lesson, user) if recap_lesson else None,
            is_completed=self._is_completed_by(unit, user),
            is_locked=is_locked
        )

    def _is_completed_by(self, unit: Unit, user: User) -> bool:
        lesson_service = LessonService(self._uow)
        return all(lesson_service._is_completed_by(self._uow.lessons.get_by_id(basic_lesson.id), user) for basic_lesson in unit.lessons)
        

    def generate_recap_lesson(self, unit: Unit, user: User) -> None:
        # Precondition: all exercises in the unit have been attempted at least once
        exercise_scores = [
            (exercise, self._uow.exercise_attempts.get_max_score_by_user_id_and_exercise_id(user.id, exercise.id)) 
            for basic_lesson in unit.lessons 
            for exercise in self._uow.lessons.get_by_id(basic_lesson.id).exercises]

        exercise_scores.sort(key=lambda x: x[1])
        exercises = [exercise for exercise, _ in exercise_scores[:5]]
        lesson = self._uow.lessons.upsert(Lesson(
            title=f"Recap of {unit.name}",
            exercises=[Exercise(index=i, word_id=exercise.word_id) for i, exercise in enumerate(exercises)],
        ))
        self._uow.recap_lessons.upsert(RecapLesson(
            id=lesson.id,
            unit_id=unit.id,
            user_id=user.id
        ))
        self._uow.commit()
