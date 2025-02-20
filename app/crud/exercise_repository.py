
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.generic_repository import GenericRepository
from app.models.exercise import Exercise


class ExerciseRepository(GenericRepository[Exercise]):

    def __init__(self, session: AsyncSession):
        super().__init__(session, Exercise)

    