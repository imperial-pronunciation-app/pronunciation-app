from app.crud.unit_of_work import UnitOfWork
from app.models.unit import Unit
from app.models.user import User
from app.schemas.unit import UnitPublicWithLessons
from app.services.lesson import LessonService


class UnitService:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow
    
    async def to_public_with_lessons(self, unit: Unit, user: User) -> UnitPublicWithLessons:
        lesson_service = LessonService(self._uow)
        return UnitPublicWithLessons(
            id=unit.id,
            name=unit.name,
            description=unit.description,
            lessons=[(await lesson_service.to_response(lesson, user)) for lesson in unit.lessons]
        )