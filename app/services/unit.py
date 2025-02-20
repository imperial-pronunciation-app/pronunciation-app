from app.crud.unit_of_work import UnitOfWork
from app.models.lesson import Lesson
from app.models.unit import Unit
from app.models.user import User
from app.schemas.unit import UnitPublicWithLessons
from app.services.lesson import LessonService


class UnitService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow
    
    def to_public_with_lessons(self, unit: Unit, user: User) -> UnitPublicWithLessons:
        lesson_service = LessonService(self._uow)
        return UnitPublicWithLessons(
            id=unit.id,
            name=unit.name,
            description=unit.description,
            lessons=[lesson_service.to_response(lesson, user) for lesson in unit.lessons],
            recap_lesson=self._uow.lessons.find_recap_by_user_id_and_unit_id(user.id, unit.id)
        )
        

    def generate_recap_lesson(self, unit: Unit, user: User) -> Lesson:
        exercise_scores = [(exercise, self._uow.attempts.get_max_score_by_user_id_and_exercise_id(user.id, exercise.id)) for lesson in unit.lessons for exercise in lesson.exercises]
        exercise_scores.sort(key=lambda x: x[1])
        exercises = [exercise for exercise, _ in exercise_scores[:5]]
        return Lesson(
            title=f"Recap of {unit.name}",
            unit=unit,
            exercises=exercises,
            user_id=user.id
        )