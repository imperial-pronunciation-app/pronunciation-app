from app.crud.unit_of_work import UnitOfWork
from app.models.basic_lesson import BasicLesson
from app.models.recap_lesson import RecapLesson
from app.models.user import User
from app.schemas.lesson import ListedLessonResponse
from app.services.lesson import LessonService


class RecapLessonService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow
    
    def to_response(self, recap: RecapLesson, user: User) -> ListedLessonResponse:
        lesson = self._uow.lessons.get_by_id(recap.id)
        prev_basic_lesson = self.prev_lesson(recap)
        prev_lesson = self._uow.lessons.get_by_id(prev_basic_lesson.id) if prev_basic_lesson else None
        return LessonService(self._uow).to_listed_response(lesson, user, prev_lesson)
    
    def prev_lesson(self, recap: RecapLesson) -> BasicLesson | None:
        return recap.unit.lessons[-1]