
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.generic_repository import GenericRepository
from app.models.lesson import Lesson


class LessonRepository(GenericRepository[Lesson]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, Lesson)

    