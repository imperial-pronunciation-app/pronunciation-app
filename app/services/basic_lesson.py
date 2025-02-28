from app.crud.unit_of_work import UnitOfWork
from app.models.basic_lesson import BasicLesson
from app.models.user import User
from app.schemas.lesson import ListedLessonResponse
from app.services.lesson import LessonService


class BasicLessonService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    def to_response(self, basic: BasicLesson, user: User) -> ListedLessonResponse:
        lesson = self._uow.lessons.get_by_id(basic.id)
        prev_basic_lesson = self.prev_lesson(basic)
        prev_lesson = self._uow.lessons.get_by_id(prev_basic_lesson.id) if prev_basic_lesson else None
        return LessonService(self._uow).to_listed_response(lesson, user, prev_lesson)

    def prev_lesson(self, basic: BasicLesson) -> BasicLesson | None:
        return basic.unit.lessons[basic.index - 1] if basic.index > 0 else None